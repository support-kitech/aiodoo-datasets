# Developer Guide

## Creating a new Processor
Processors must be entirely stateless and operate purely by mutating and re-returning the `ProcessorContext`.

1. **Inherit `BaseProcessor`**: All processors must inherit from `preprocessing.processors.base.BaseProcessor`.
2. **Assign Priority**: Utilize a priority constant from `preprocessing.constants.framework`.
3. **Purity Rule**: Do not perform I/O. Do not mutate existing state. Instead, use `context.with_update(current_content=new_string)`.
4. **Register**: Add the processor to `PreprocessingManager._build_default_registry()`. Order does not matter, the registry sorts via Priority at `freeze()`.
