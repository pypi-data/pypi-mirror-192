from django.forms import CharField, BooleanField

from netbox.forms import NetBoxModelFilterSetForm
from ocp_project_plugin.choices import AppEnvironmentClusterEnvChoices, AppEnvironmentDeploymentKindChoices
from ocp_project_plugin.models import AppEnvironment, OCPProject
from utilities.forms import MultipleChoiceField, DynamicModelMultipleChoiceField


class AppEnvironmentFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering App Environment instances."""

    model = AppEnvironment
    fieldsets = (
        (None, ('q', 'filter_id')),
        ('OCP Project', ['ocp_project']),
        ('Environment', ('cluster_env', 'app_env')),
        ('Deployment', ('repo', 'branch', 'access_token', 'path', 'deployment_kind')),
        ('Monitoring', ('monitoring', 'postgres_monitoring')),
        ('Resources', ('limits_cpu', 'limits_memory', 'requests_cpu', 'requests_memory')),
        ('Additional Config', ('mtls', 'egress_ip')),
    )
    cluster_env = MultipleChoiceField(
        choices=AppEnvironmentClusterEnvChoices,
        required=False
    )
    app_env = CharField(
        required=False,
        label="App Env",
        help_text="The app Env String used for creating the namespace e.g. tst",
    )
    mtls = BooleanField(
        required=False,
        label="MTLS",
        help_text="Enable if mtls should be used",
    )
    repo = CharField(
        required=False,
        label="Git Repository",
        help_text="Path of git Repository, don't forget the .git at the end e.g. "
                  "https://gitlab.com/example/example-deployment-manifests.git",
    )
    branch = CharField(
        required=False,
        label="Git Branch",
        help_text="The git Branch of the Repository e.g. main"
    )
    path = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    egress_ip = CharField(
        required=False,
        label="Egress IP",
        help_text="The egress IP e.g. 10.10.10.10"
    )
    monitoring = BooleanField(
        required=False,
        label="Monitoring",
        help_text="Enable if monitoring should be used",
    )
    postgres_monitoring = BooleanField(
        required=False,
        label="Postgres Monitoring",
        help_text="Enable if postgres monitoring should be used",
    )
    access_token = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    limits_cpu = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    limits_memory = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    requests_cpu = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    requests_memory = CharField(
        required=False,
        label="Git Path",
        help_text="Path of the deployment files e.g. overlays/tst"
    )
    deployment_kind = MultipleChoiceField(
        choices=AppEnvironmentDeploymentKindChoices,
        required=False
    )
    ocp_project = DynamicModelMultipleChoiceField(
        queryset=OCPProject.objects.all(),
        required=False,
        label='OCP Project'
    )
