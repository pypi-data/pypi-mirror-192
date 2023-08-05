from django.forms import (
    CharField,
    BooleanField, PasswordInput, ModelChoiceField,
)

from ipam.models import Prefix, IPAddress
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from ocp_project_plugin.choices import AppEnvironmentClusterEnvChoices, AppEnvironmentDeploymentKindChoices
from ocp_project_plugin.models import AppEnvironment, OCPProject
from utilities.forms import DynamicModelChoiceField, APISelectMultiple, CSVModelChoiceField, MultipleChoiceField, \
    DynamicModelMultipleChoiceField




class AppEnvironmentBulkEditForm(NetBoxModelBulkEditForm):
    model = AppEnvironment

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
