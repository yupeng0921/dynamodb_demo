#! /bin/bash

{% for server in servers %}
/usr/bin/aws autoscaling enter-standby --instance-ids {{server}} --auto-scaling-group-name {{server_asg_name}} --should-decrement-desired-capacity --region {{region}}
{% endfor %}

{% for client in clients %}
/usr/bin/aws autoscaling enter-standby --instance-ids {{client}} --auto-scaling-group-name {{client_asg_name}} --should-decrement-desired-capacity --region {{region}}
{% endfor %}
