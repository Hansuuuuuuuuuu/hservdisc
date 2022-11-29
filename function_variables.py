#target group mapping
target_groups = {
	'service:<NAME OF SERVICE>': 'arn:aws:elasticloadbalancing:<REGION>:<ACCOUNT ID>:targetgroup/<TARGET GROUP>',
	'service:hello-world': 'arn:aws:elasticloadbalancing:ap-southeast-1:123456789:targetgroup/test-hello-world/123456789',
}

#array of monitored clusters

clusters = [
	"arn:aws:ecs:ap-southeast-1:<ACCOUNT ID>:cluster/<CLUSTER NAME HERE>",
	"arn:aws:ecs:ap-southeast-1:123456789:cluster/Hello-World-Cluster"
]