//===----------------------------------------------------------------------===//
//
// Copyright (C) 2022 Sophgo Technologies Inc.  All rights reserved.
//
// TPU-MLIR is licensed under the 2-Clause BSD License except for the
// third-party components.
//
//===----------------------------------------------------------------------===//
#include <fstream>
#include <set>
#include <sstream>
#include <vector>
#include "tpu_mlir/Dialect/Tpu/Transforms/GdmaIrgen.hpp"
#include "tpu_mlir/Dialect/Tpu/Transforms/DynCompileCommon.hpp"
#include "tpu_mlir/Dialect/Tpu/Transforms/DynamicLayer.hpp"
#include "tpu_mlir/Backend/BM168x/BM1684X.h"
#include "tpu_mlir/Support/Module.h"

using namespace tpu_mlir::backend;
namespace tpu_mlir {
namespace tpu {
DATA_SIZE_T get_dynamic_compiler_tensor_datasize(int data_type)
{
  DATA_SIZE_T data_size;
  switch(data_type) {
    case DTYPE_INT8:
    case DTYPE_UINT8:
      data_size = DSIZE_8;
      break;
    case DTYPE_INT16:
    case DTYPE_UINT16:
    case DTYPE_FP16:
    case DTYPE_BFP16:
      data_size = DSIZE_16;
      break;
    case DTYPE_INT32:
    case DTYPE_UINT32:
      data_size = DSIZE_INT32;
      break;
    default:
      data_size = DSIZE_FP32;
      break;
  }
  return data_size;
}

int static_ld_coeff_irgen_ctrl(
    Operation *op,
    int tensor_id, uint64_t global_addr,
    uint64_t local_addr,
    ir_tensor_gdma_info_t& ir_tensor_gdma_info,
    int dynamic_ver
  ) {
  int fw_ir_length = 0;
  ir_tensor_gdma_info.fw_tensor_gdma_type = LD_COEFF;
  fw_gdma_coeff_t fw_gdma_coeff = {0};
  int64_t N, C, H, W;
  module::getNCHW(op->getOperand(0), N, C, H, W);
  uint32_t ic = N;
  uint32_t oc = C;
  uint32_t kh = H;
  uint32_t kw = W;
  auto lgOp = dyn_cast<DynLocalGenInterface>(op);
  auto ginfo = lgOp.DynGetGroupInfo((int64_t)0, (int64_t)0);
  uint8_t one_time = (ginfo.h_slice == H);

  int c_idx = 0;
  fw_gdma_coeff.global_offset = global_addr;
  fw_gdma_coeff.local_offset = local_addr + (c_idx % BM168x::NPU_NUM) * (BM168x::LMEM_BYTES);
  fw_gdma_coeff.ic_oc = (ic << 16) | oc;
  fw_gdma_coeff.kh_kw = (kh << 16) | kw;
  fw_gdma_coeff.one_time = one_time;
  fw_gdma_coeff.winograd_coeff = 0;
  fw_gdma_coeff.groups = 1;
  fw_gdma_coeff.data_size = get_dynamic_compiler_tensor_datasize(BM168x::getDataType(op->getOperand(0)));
  if (dynamic_ver) {
      fw_gdma_coeff.dtype = BM168x::getDataType(op->getOperand(0));
  }

  auto use_op = *op->getUsers().begin();
  if (auto conv_op = dyn_cast<tpu::Conv1DOp>(use_op)) {
    if (module::isUniformQuantized(conv_op.getInput())) {
      if (conv_op.getCoeffMerged()) {
        fw_gdma_coeff.winograd_coeff = 2;
      }
    }
    fw_gdma_coeff.groups = conv_op.getGroup();
    fw_gdma_coeff.layer_type = get_layer_type(conv_op);
  } else if (auto conv_op = dyn_cast<tpu::Conv1DOp>(use_op)) {
    if (module::isUniformQuantized(conv_op.getInput())) {
      if (conv_op.getCoeffMerged()) {
        fw_gdma_coeff.winograd_coeff = 2;
      }
    }
    fw_gdma_coeff.groups = conv_op.getGroup();
    fw_gdma_coeff.layer_type = get_layer_type(conv_op);
  } else if (auto conv_op = dyn_cast<tpu::Conv3DOp>(use_op)) {
    fw_gdma_coeff.groups = conv_op.getGroup();
    fw_gdma_coeff.layer_type = get_layer_type(conv_op);
  }

  fw_gdma_coeff.depth = 1;
  ir_tensor_gdma_info.fw_tensor_gdma_param_u.fw_gdma_coeff = fw_gdma_coeff;
  fw_ir_length += sizeof(fw_gdma_coeff_t);
  return fw_ir_length;
}

int static_ld_neuron_irgen_ctrl(
    Operation *op,
    int tensor_id, uint64_t global_addr,
    uint64_t local_addr,
    ir_tensor_gdma_info_t& ir_tensor_gdma_info,
    int dynamic_ver
  )
{
  int fw_ir_length = 0;
  int64_t N, C, H, W;
  module::getNCHW(op->getOperand(0), N, C, H, W);

  uint32_t ic = (uint32_t)(C);
  int out_tensor_id=0,c_idx=0;
  out_tensor_id = get_tensor_id(op->getResult(0));
  int consumer_num = 0;
  for (auto v: op->getResult(0).getUsers()) {
    consumer_num++;
    (void)(v);
  }

  u32 local_mem_offset = local_addr;

  if(!is_net_input(op->getOperand(0))) {
    //itm neuron
    ir_tensor_gdma_info.fw_tensor_gdma_type = LD_ITM_EXTEND_NEURON;

    fw_gdma_ld_itm_extend_neuron_t fw_gdma_ld_itm_extend_neuron = {0};
    fw_gdma_ld_itm_extend_neuron.global_offset = global_addr;
    fw_gdma_ld_itm_extend_neuron.local_offset = local_mem_offset;
    fw_gdma_ld_itm_extend_neuron.c_idx = c_idx;
    fw_gdma_ld_itm_extend_neuron.reference_id = tensor_id;
    fw_gdma_ld_itm_extend_neuron.ic = ic;
    fw_gdma_ld_itm_extend_neuron.tensor_id = out_tensor_id;
    fw_gdma_ld_itm_extend_neuron.concat_c = 0;
    fw_gdma_ld_itm_extend_neuron.data_size = get_dynamic_compiler_tensor_datasize(BM168x::getDataType(op->getOperand(0)));
    if (dynamic_ver) {
        fw_gdma_ld_itm_extend_neuron.dtype = BM168x::getDataType(op->getOperand(0));
    }

    fw_gdma_ld_itm_extend_neuron.store_mode = STORE_MODE_1N;
    fw_gdma_ld_itm_extend_neuron.consumer_num = consumer_num;
    ir_tensor_gdma_info.fw_tensor_gdma_param_u.fw_gdma_ld_itm_extend_neuron = fw_gdma_ld_itm_extend_neuron;
    fw_ir_length += sizeof(fw_gdma_ld_itm_extend_neuron_t);
  } else {
    //in neuron
    ir_tensor_gdma_info.fw_tensor_gdma_type = LD_INPUT_NEURON;

    fw_gdma_ld_in_neuron_t fw_gdma_ld_in_neuron = {0};
    fw_gdma_ld_in_neuron.local_offset = local_mem_offset;
    fw_gdma_ld_in_neuron.c_idx_and_reference_id = (c_idx << 16) | (uint32_t)tensor_id;
    fw_gdma_ld_in_neuron.ic_and_tensor_id = (ic << 16) | (uint32_t)out_tensor_id;
    fw_gdma_ld_in_neuron.concat_c = 0;
    fw_gdma_ld_in_neuron.data_size = get_dynamic_compiler_tensor_datasize(BM168x::getDataType(op->getOperand(0)));
    if (dynamic_ver) {
        fw_gdma_ld_in_neuron.dtype = BM168x::getDataType(op->getOperand(0));
    }

    fw_gdma_ld_in_neuron.store_mode = STORE_MODE_1N;
    fw_gdma_ld_in_neuron.consumer_num = consumer_num;
    ir_tensor_gdma_info.fw_tensor_gdma_param_u.fw_gdma_ld_in_neuron = fw_gdma_ld_in_neuron;
    fw_ir_length += sizeof(fw_gdma_ld_in_neuron_t);
  }

  return fw_ir_length;
}

int static_st_neuron_irgen_ctrl(
    Operation *op,
    int tensor_id, uint64_t global_addr,
    uint64_t local_addr,
    ir_tensor_gdma_info_t& ir_tensor_gdma_info,
    int dynamic_ver
  ) {
  int fw_ir_length = 0;
  uint64_t global_mem_offset = global_addr;
  uint32_t local_mem_offset = 0;
  //int c_idx_in = 0, concattensor_id = 0;
  bool mem_is_set=false;
  int64_t N, ic, height, width;
  module::getNCHW(op->getResult(0), N, ic, height, width);

  if (mem_is_set == false) {
    local_mem_offset = local_addr;
  }

  int concat_c = 0;
  int c_idx = 0;
  int concat_tensor_id = 0;

  u32 merge_npu_c = 0;
  u32 split_c_num = 0;

  // Wheter or not the tensor_id is one of the network outputs?
  bool is_tensor_output = is_net_output(op->getResult(0));

  // Whether or not the concat_tensor_id (if not 0) is one of the network outputs?
  bool is_concat_tensor_output = false;

  if(!is_tensor_output && !is_concat_tensor_output) {
    if (concat_c > 65535 || ic > 65535) {
      //itm extend neruon
      ir_tensor_gdma_info.fw_tensor_gdma_type = ST_ITM_EXTEND_NEURON;

      fw_gdma_st_itm_extend_neuron_t fw_gdma_st_itm_extend_neuron = {0};
      fw_gdma_st_itm_extend_neuron.global_offset = global_mem_offset;
      fw_gdma_st_itm_extend_neuron.local_offset = local_mem_offset;
      fw_gdma_st_itm_extend_neuron.ic = ic;
      fw_gdma_st_itm_extend_neuron.tensor_id = (uint32_t)tensor_id;
      fw_gdma_st_itm_extend_neuron.concat_c = (uint32_t)concat_c;
      fw_gdma_st_itm_extend_neuron.cidx = (uint32_t)c_idx;
      fw_gdma_st_itm_extend_neuron.concat_tensor_id = (uint32_t)concat_tensor_id;
      fw_gdma_st_itm_extend_neuron.merge_npu_c = (uint32_t)merge_npu_c;
      fw_gdma_st_itm_extend_neuron.split_c_num = (uint32_t)split_c_num;
      fw_gdma_st_itm_extend_neuron.data_size = get_dynamic_compiler_tensor_datasize(BM168x::getDataType(op->getResult(0)));
      if (dynamic_ver) {
          fw_gdma_st_itm_extend_neuron.dtype = BM168x::getDataType(op->getResult(0));
      }

      fw_gdma_st_itm_extend_neuron.store_mode = STORE_MODE_1N;
      ir_tensor_gdma_info.fw_tensor_gdma_param_u.fw_gdma_st_itm_extend_neuron = fw_gdma_st_itm_extend_neuron;
      fw_ir_length += sizeof(fw_gdma_st_itm_extend_neuron_t);
    } else {
      //itm neruon
      ir_tensor_gdma_info.fw_tensor_gdma_type = ST_ITM_NEURON;

      fw_gdma_st_itm_neuron_t fw_gdma_st_itm_neuron = {0};

      fw_gdma_st_itm_neuron.global_offset = global_mem_offset;
      fw_gdma_st_itm_neuron.local_offset = local_mem_offset;
      fw_gdma_st_itm_neuron.ic_and_tensor_id = (ic << 16) | (uint32_t)tensor_id;
      fw_gdma_st_itm_neuron.concat_c_and_cidx = ((uint32_t)concat_c << 16) | ((uint32_t)c_idx);
      fw_gdma_st_itm_neuron.concat_tensor_id = (uint32_t)concat_tensor_id;
      fw_gdma_st_itm_neuron.merge_npu_c = (uint8_t)merge_npu_c;
      fw_gdma_st_itm_neuron.split_c_num = (uint8_t)split_c_num;
      fw_gdma_st_itm_neuron.data_size = get_dynamic_compiler_tensor_datasize(BM168x::getDataType(op->getResult(0)));
      if (dynamic_ver) {
          fw_gdma_st_itm_neuron.dtype = BM168x::getDataType(op->getResult(0));
      }
      fw_gdma_st_itm_neuron.store_mode = STORE_MODE_1N;
      ir_tensor_gdma_info.fw_tensor_gdma_param_u.fw_gdma_st_itm_neuron = fw_gdma_st_itm_neuron;
      fw_ir_length += sizeof(fw_gdma_st_itm_neuron_t);
    }
  } else {
    if (concat_c > 65535 || ic > 65535) {
      //out neuron
      ir_tensor_gdma_info.fw_tensor_gdma_type = ST_OUTPUT_EXTEND_NEURON;

      fw_gdma_st_out_extend_neuron_t fw_gdma_st_out_extend_neuron = {0};
      fw_gdma_st_out_extend_neuron.local_offset = local_mem_offset;
      fw_gdma_st_out_extend_neuron.tensor_id = (uint32_t)tensor_id;
      fw_gdma_st_out_extend_neuron.ic = ic;
      fw_gdma_st_out_extend_neuron.cidx = (uint32_t)c_idx;
      fw_gdma_st_out_extend_neuron.concat_c = (uint32_t)concat_c;
      fw_gdma_st_out_extend_neuron.concat_tensor_id = (uint32_t)concat_tensor_id;
      fw_gdma_st_out_extend_neuron.merge_npu_c = (uint8_t)merge_npu_c;
      fw_gdma_st_out_extend_neuron.split_c_num = (uint8_t)split_c_num;
      fw_gdma_st_out_extend_neuron.data_size = get_dynamic_compiler_tensor_datasize(BM168x::getDataType(op->getResult(0)));
      if (dynamic_ver) {
          fw_gdma_st_out_extend_neuron.dtype = BM168x::getDataType(op->getResult(0));
      }
      fw_gdma_st_out_extend_neuron.store_mode = STORE_MODE_1N;
      ir_tensor_gdma_info.fw_tensor_gdma_param_u.fw_gdma_st_out_extend_neuron = fw_gdma_st_out_extend_neuron;
      fw_ir_length += sizeof(fw_gdma_st_out_extend_neuron_t);
    } else {
      //out neuron
      ir_tensor_gdma_info.fw_tensor_gdma_type = ST_OUTPUT_NEURON;

      fw_gdma_st_out_neuron_t fw_gdma_st_out_neuron = {0};
      fw_gdma_st_out_neuron.local_offset = local_mem_offset;
      fw_gdma_st_out_neuron.ic_and_tensor_id = (ic << 16) | (uint32_t)tensor_id;
      fw_gdma_st_out_neuron.concat_c_and_cidx = ((uint32_t)concat_c << 16) | ((uint32_t)c_idx);
      fw_gdma_st_out_neuron.concat_tensor_id = (uint32_t)concat_tensor_id;
      fw_gdma_st_out_neuron.merge_npu_c = (uint8_t)merge_npu_c;
      fw_gdma_st_out_neuron.split_c_num = (uint8_t)split_c_num;
      fw_gdma_st_out_neuron.data_size = get_dynamic_compiler_tensor_datasize(BM168x::getDataType(op->getResult(0)));
      if (dynamic_ver) {
          fw_gdma_st_out_neuron.dtype = BM168x::getDataType(op->getResult(0));
      }
      fw_gdma_st_out_neuron.store_mode = STORE_MODE_1N;
      ir_tensor_gdma_info.fw_tensor_gdma_param_u.fw_gdma_st_out_neuron = fw_gdma_st_out_neuron;
      fw_ir_length += sizeof(fw_gdma_st_out_neuron_t);
    }
  }
  return fw_ir_length;
}
}
}
