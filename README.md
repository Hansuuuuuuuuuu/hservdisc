# HServDisc

#### _This is mostly for archival purposes as [AWS now supports adding multiple target groups to ECS services](https://aws.amazon.com/about-aws/whats-new/2019/07/amazon-ecs-services-now-support-multiple-load-balancer-target-groups/)._

HServDisc allows you to attach ECS services to a specified Target Group automatically. This was created due to a limitation on AWS' side which meant that only one target group can be associated to a service, thereby affecting setups that require different public and private load balancers. 

## How It Works

HServDisc is triggered by an ECS Task State Change rule on SNS. It then checks if the cluster is being monitored (under `clusters` on `function_variables`) and there is a corresponding target group mapping for the task's service. 
If the state change's `lastStatus` and `desiredStatus` are both `RUNNING`, HServDisc will register that target on the appropriate target group.
If the state change's `lastStatus` is `RUNNING` and the `desiredStatus` is `STOPPED`, the target will be deregistered from the appropriate target group.