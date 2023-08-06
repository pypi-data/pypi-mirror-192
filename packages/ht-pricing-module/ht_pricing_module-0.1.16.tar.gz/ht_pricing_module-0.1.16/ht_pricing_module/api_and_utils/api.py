from ht_pricing_module.api_and_utils.packages import grpc

protos_pricer, services_pricer = grpc.protos_and_services('ht_pricing_module/api_and_utils/protos/pricer.proto')

# 'CONTINUOUS', 'DISCRETE'
ObsType = protos_pricer.ObsType

# 'CALL', 'PUT', 'ACCUMULATOR', 'DECUMULATOR', 'STANDARD', 'REVERSE', 'ONE_TOUCH', 'DOUBLE_ONE_TOUCH
OptionType = protos_pricer.OptionType

# 'EUROPEAN', 'AMERICAN'
ExerciseType = protos_pricer.ExerciseType

# 'UP', 'DOWN'
BarrierType = protos_pricer.BarrierType

# 'IN', 'OUT'
KnockType = protos_pricer.KnockType

# 'PAH', 'PAE'
RebateType = protos_pricer.RebateType

# 'AS', 'MC', 'PDE'
PricingMethod = protos_pricer.PricingMethod

# 'LINEAR_ACC', 'FIXED_ACC', 'FIXED_ACC_AKO', 'FIXED_ACC_BARRIER', 'LINEAR_ACC_ENHANCED'
AccumulatorType = protos_pricer.AccumulatorType
