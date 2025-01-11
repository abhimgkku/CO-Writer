class IAutoScalingClient:
    def register_scalable_target(self, **kwargs):
        raise NotImplementedError

    def put_scaling_policy(self, **kwargs):
        raise NotImplementedError

    def describe_scalable_targets(self, **kwargs):
        raise NotImplementedError

    def describe_scaling_policies(self, **kwargs):
        raise NotImplementedError

    def delete_scaling_policy(self, **kwargs):
        raise NotImplementedError

    def deregister_scalable_target(self, **kwargs):
        raise NotImplementedError


class ScalingPolicyStrategy:
    def apply_policy(self):
        raise NotImplementedError


class TargetTrackingScalingPolicy(ScalingPolicyStrategy):
    def __init__(
        self,
        auto_scaling_client: IAutoScalingClient,
        policy_name: str,
        service_namespace: str,
        resource_id: str,
        scalable_dimension: str,
        target_value: float,
        scale_in_cooldown: int,
        scale_out_cooldown: int,
    ):
        self.aas_client = auto_scaling_client
        self.policy_name = policy_name
        self.service_namespace = service_namespace
        self.resource_id = resource_id
        self.scalable_dimension = scalable_dimension
        self.target_value = target_value
        self.scale_in_cooldown = scale_in_cooldown
        self.scale_out_cooldown = scale_out_cooldown

    def apply_policy(self):
        self.aas_client.put_scaling_policy(
            PolicyName=self.policy_name,
            PolicyType="TargetTrackingScaling",
            ServiceNamespace=self.service_namespace,
            ResourceId=self.resource_id,
            ScalableDimension=self.scalable_dimension,
            TargetTrackingScalingPolicyConfiguration={
                "PredefinedMetricSpecification": {
                    "PredefinedMetricType": "SageMakerInferenceComponentInvocationsPerCopy",
                },
                "TargetValue": self.target_value,
                "ScaleInCooldown": self.scale_in_cooldown,
                "ScaleOutCooldown": self.scale_out_cooldown,
            },
        )


class ScalableTarget:
    def __init__(
        self,
        auto_scaling_client: IAutoScalingClient,
        service_namespace: str,
        resource_id: str,
        scalable_dimension: str,
        min_capacity: int,
        max_capacity: int,
    ):
        self.aas_client = auto_scaling_client
        self.service_namespace = service_namespace
        self.resource_id = resource_id
        self.scalable_dimension = scalable_dimension
        self.min_capacity = min_capacity
        self.max_capacity = max_capacity

    def register(self):
        self.aas_client.register_scalable_target(
            ServiceNamespace=self.service_namespace,
            ResourceId=self.resource_id,
            ScalableDimension=self.scalable_dimension,
            MinCapacity=self.min_capacity,
            MaxCapacity=self.max_capacity,
        )


class AutoscalingSagemakerEndpoint:
    def __init__(
        self,
        auto_scaling_client: IAutoScalingClient,
        inference_component_name: str,
        endpoint_name: str,
        initial_copy_count: int = 1,
        max_copy_count: int = 6,
        target_value: float = 4.0,
    ):
        self.auto_scaling_client = auto_scaling_client
        self.inference_component_name = inference_component_name
        self.endpoint_name = endpoint_name
        self.initial_copy_count = initial_copy_count
        self.max_copy_count = max_copy_count
        self.target_value = target_value
        self.service_namespace = "sagemaker"
        self.scalable_dimension = "sagemaker:inference-component:DesiredCopyCount"
        self.resource_id = f"inference-component/{self.inference_component_name}"

    def setup_autoscaling(self):
        # Register scalable target
        scalable_target = ScalableTarget(
            auto_scaling_client=self.auto_scaling_client,
            service_namespace=self.service_namespace,
            resource_id=self.resource_id,
            scalable_dimension=self.scalable_dimension,
            min_capacity=self.initial_copy_count,
            max_capacity=self.max_copy_count,
        )
        scalable_target.register()

        # Add scaling policy
        policy = TargetTrackingScalingPolicy(
            auto_scaling_client=self.auto_scaling_client,
            policy_name=self.endpoint_name,
            service_namespace=self.service_namespace,
            resource_id=self.resource_id,
            scalable_dimension=self.scalable_dimension,
            target_value=self.target_value + 1,  # Example adjustment, should be based on specific use case
            scale_in_cooldown=200,
            scale_out_cooldown=200,
        )
        policy.apply_policy()

    def cleanup_autoscaling(self):
        # Remove scaling policy
        self.auto_scaling_client.delete_scaling_policy(
            PolicyName=self.endpoint_name,
            ServiceNamespace=self.service_namespace,
            ResourceId=self.resource_id,
            ScalableDimension=self.scalable_dimension,
        )

        # Deregister scalable target
        self.auto_scaling_client.deregister_scalable_target(
            ServiceNamespace=self.service_namespace,
            ResourceId=self.resource_id,
            ScalableDimension=self.scalable_dimension,
        )
