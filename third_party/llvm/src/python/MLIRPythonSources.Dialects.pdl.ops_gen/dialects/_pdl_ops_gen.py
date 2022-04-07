
# Autogenerated by mlir-tblgen; don't manually edit.

from ._ods_common import _cext as _ods_cext
from ._ods_common import extend_opview_class as _ods_extend_opview_class, segmented_accessor as _ods_segmented_accessor, equally_sized_accessor as _ods_equally_sized_accessor, get_default_loc_context as _ods_get_default_loc_context, get_op_result_or_value as _get_op_result_or_value, get_op_results_or_values as _get_op_results_or_values
_ods_ir = _ods_cext.ir

try:
  from . import _pdl_ops_ext as _ods_ext_module
except ImportError:
  _ods_ext_module = None

import builtins


@_ods_cext.register_dialect
class _Dialect(_ods_ir.Dialect):
  DIALECT_NAMESPACE = "pdl"
  pass


@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ApplyNativeConstraintOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.apply_native_constraint"

  _ODS_REGIONS = (0, True)

  def __init__(self, name, args, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(args))
    attributes["name"] = name
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def args(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def name(self):
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ApplyNativeRewriteOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.apply_native_rewrite"

  _ODS_REGIONS = (0, True)

  def __init__(self, results_, name, args, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(args))
    attributes["name"] = name
    results.extend(results_)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def args(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def name(self):
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

  @builtins.property
  def results_(self):
    _ods_variadic_group_length = len(self.operation.results) - 1 + 1
    return self.operation.results[0:0 + _ods_variadic_group_length]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class AttributeOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.attribute"

  _ODS_REGIONS = (0, True)

  def __init__(self, attr, type, value, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    if type is not None: operands.append(_get_op_result_or_value(type))
    if value is not None: attributes["value"] = value
    results.append(attr)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def type(self):
    return None if len(self.operation.operands) < 1 else self.operation.operands[0]

  @builtins.property
  def value(self):
    if "value" not in self.operation.attributes:
      return None
    return _ods_ir.Attribute(self.operation.attributes["value"])

  @value.setter
  def value(self, value):
    if value is not None:
      self.operation.attributes["value"] = value
    elif "value" in self.operation.attributes:
      del self.operation.attributes["value"]

  @value.deleter
  def value(self):
    del self.operation.attributes["value"]

  @builtins.property
  def attr(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class EraseOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.erase"

  _ODS_REGIONS = (0, True)

  def __init__(self, operation_, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(operation_))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def operation_(self):
    return self.operation.operands[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class OperandOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.operand"

  _ODS_REGIONS = (0, True)

  def __init__(self, val, type, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    if type is not None: operands.append(_get_op_result_or_value(type))
    results.append(val)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def type(self):
    return None if len(self.operation.operands) < 1 else self.operation.operands[0]

  @builtins.property
  def val(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class OperandsOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.operands"

  _ODS_REGIONS = (0, True)

  def __init__(self, val, type, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    if type is not None: operands.append(_get_op_result_or_value(type))
    results.append(val)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def type(self):
    return None if len(self.operation.operands) < 1 else self.operation.operands[0]

  @builtins.property
  def val(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class OperationOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.operation"

  _ODS_OPERAND_SEGMENTS = [-1,-1,-1,]

  _ODS_REGIONS = (0, True)

  def __init__(self, op, name, operands_, attributes_, attributeNames, types, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_results_or_values(operands_))
    operands.append(_get_op_results_or_values(attributes_))
    operands.append(_get_op_results_or_values(types))
    if name is not None: attributes["name"] = name
    attributes["attributeNames"] = attributeNames
    results.append(op)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def operands_(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 0)
    return operand_range

  @builtins.property
  def attributes_(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 1)
    return operand_range

  @builtins.property
  def types(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 2)
    return operand_range

  @builtins.property
  def name(self):
    if "name" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is not None:
      self.operation.attributes["name"] = value
    elif "name" in self.operation.attributes:
      del self.operation.attributes["name"]

  @name.deleter
  def name(self):
    del self.operation.attributes["name"]

  @builtins.property
  def op(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class PatternOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.pattern"

  _ODS_REGIONS = (1, True)

  def __init__(self, benefit, sym_name, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    attributes["benefit"] = benefit
    if sym_name is not None: attributes["sym_name"] = sym_name
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def benefit(self):
    return _ods_ir.IntegerAttr(self.operation.attributes["benefit"])

  @benefit.setter
  def benefit(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["benefit"] = value

  @builtins.property
  def sym_name(self):
    if "sym_name" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is not None:
      self.operation.attributes["sym_name"] = value
    elif "sym_name" in self.operation.attributes:
      del self.operation.attributes["sym_name"]

  @sym_name.deleter
  def sym_name(self):
    del self.operation.attributes["sym_name"]

  @builtins.property
  def body(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ReplaceOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.replace"

  _ODS_OPERAND_SEGMENTS = [1,0,-1,]

  _ODS_REGIONS = (0, True)

  def __init__(self, operation_, replOperation, replValues, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(operation_))
    operands.append(_get_op_result_or_value(replOperation) if replOperation is not None else None)
    operands.append(_get_op_results_or_values(replValues))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def operation_(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 0)
    return operand_range[0]

  @builtins.property
  def replOperation(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 1)
    return operand_range[0] if len(operand_range) > 0 else None

  @builtins.property
  def replValues(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 2)
    return operand_range

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ResultOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.result"

  _ODS_REGIONS = (0, True)

  def __init__(self, val, parent, index, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(parent))
    attributes["index"] = index
    results.append(val)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def parent(self):
    return self.operation.operands[0]

  @builtins.property
  def index(self):
    return _ods_ir.IntegerAttr(self.operation.attributes["index"])

  @index.setter
  def index(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["index"] = value

  @builtins.property
  def val(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ResultsOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.results"

  _ODS_REGIONS = (0, True)

  def __init__(self, val, parent, index, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(parent))
    if index is not None: attributes["index"] = index
    results.append(val)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def parent(self):
    return self.operation.operands[0]

  @builtins.property
  def index(self):
    if "index" not in self.operation.attributes:
      return None
    return _ods_ir.IntegerAttr(self.operation.attributes["index"])

  @index.setter
  def index(self, value):
    if value is not None:
      self.operation.attributes["index"] = value
    elif "index" in self.operation.attributes:
      del self.operation.attributes["index"]

  @index.deleter
  def index(self):
    del self.operation.attributes["index"]

  @builtins.property
  def val(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class RewriteOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.rewrite"

  _ODS_OPERAND_SEGMENTS = [0,-1,]

  _ODS_REGIONS = (1, True)

  def __init__(self, root, name, externalArgs, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(root) if root is not None else None)
    operands.append(_get_op_results_or_values(externalArgs))
    if name is not None: attributes["name"] = name
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def root(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 0)
    return operand_range[0] if len(operand_range) > 0 else None

  @builtins.property
  def externalArgs(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 1)
    return operand_range

  @builtins.property
  def name(self):
    if "name" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is not None:
      self.operation.attributes["name"] = value
    elif "name" in self.operation.attributes:
      del self.operation.attributes["name"]

  @name.deleter
  def name(self):
    del self.operation.attributes["name"]

  @builtins.property
  def body(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class TypeOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.type"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, type, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    if type is not None: attributes["type"] = type
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class TypesOp(_ods_ir.OpView):
  OPERATION_NAME = "pdl.types"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, types, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    if types is not None: attributes["types"] = types
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def result(self):
    return self.operation.results[0]
