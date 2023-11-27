# Generated by Django 4.2.4 on 2023-11-27 20:13

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialCompliance',
            fields=[
                ('FCDAmendmentId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ParentAmendmentId', models.UUIDField(null=True)),
                ('ParentRecord', models.BooleanField()),
                ('POnumber', models.TextField(null=True)),
                ('DateFinalInvoiceRecieved', models.DateField(null=True)),
                ('DateFinalInvoiceDue', models.DateField(null=True)),
                ('PrimeSponsorType', models.CharField(blank=True, choices=[('Federal', 'Federal'), ('NonFederal', 'Nonfederal')], max_length=255, null=True)),
                ('AwardType', models.CharField(blank=True, choices=[('Cost', 'Cost'), ('Fixed', 'Fixed')], max_length=255, null=True)),
                ('BillingTerms', models.CharField(blank=True, choices=[('Monthly', 'Monthly'), ('Quaterly', 'Quaterly'), ('Deliverable', 'Deliverable')], max_length=255, null=True)),
                ('FFATAFilledDate', models.DateField(null=True)),
                ('Notes', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubagreementTracking',
            fields=[
                ('SATAmendmentId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ParentAmendmentId', models.UUIDField(null=True)),
                ('ParentRecord', models.BooleanField()),
                ('PrimeAgreementExecutionDate', models.DateField()),
                ('SubrecipientName', models.TextField()),
                ('UEI', models.TextField()),
                ('SAMEntity', models.BooleanField()),
                ('SAMPI', models.BooleanField()),
                ('SubawardOrContract', models.BooleanField()),
                ('DateOfSubawardExecution', models.DateField()),
                ('Status', models.CharField(choices=[('Pending preaward', 'Pendingpreaward'), ('Pending NoA', 'Pendingnoa'), ('Pending PI/DA', 'Pendingpida'), ('Pending documents from Subrecipient', 'Pendingdocsubrecp'), ('Pending post Award', 'Pendingpostaward'), ('Pending PO', 'Pendingpo'), ('Pending Assessments', 'Pendingassessments'), ('Determined to be CFS', 'Determinedcfs'), ('Open Pending', 'Openpending'), ('Executed', 'Executed'), ('Preaward', 'Preaward'), ('Active', 'Active'), ('Closed', 'Closed'), ('Withdrawn', 'Withdrawn')], default='Pending preaward')),
                ('SubawardNumber', models.TextField()),
                ('PrimeAwardNumber', models.TextField()),
                ('ProjectId', models.TextField()),
                ('PSVendorId', models.TextField()),
                ('PIFirstName', models.TextField()),
                ('PILastName', models.TextField()),
                ('PrimeSponsor', models.TextField()),
                ('FFATA', models.BooleanField()),
                ('IncrementallyEstimatedTotal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('PeriodOfPerformanceStart', models.DateField()),
                ('PeriodOfPerformanceEnd', models.DateField()),
                ('EstimatedPeriodOfPerformanceStart', models.DateField()),
                ('EstimatedPeriodOfPerformanceEnd', models.DateField()),
                ('Budget', models.BooleanField()),
                ('Attachment3B', models.BooleanField()),
                ('BudgetJustificationScore', models.IntegerField()),
                ('EntityRiskAssessmentScore', models.IntegerField()),
                ('ProjectRiskAssessmentScore', models.IntegerField()),
                ('OverallRiskAssessmentScore', models.IntegerField()),
                ('USMCRiskDetermination', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])),
                ('TwentyFiveKObligation', models.BooleanField()),
                ('DocusignRouting', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), size=None)),
                ('Comments', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('FCDAmendmentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='subawardBackend.financialcompliance')),
            ],
        ),
        migrations.AddField(
            model_name='financialcompliance',
            name='SATAmendmentId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='subawardBackend.subagreementtracking'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=300)),
                ('last_name', models.CharField(max_length=300)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=True)),
                ('date_joined', models.DateField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Users',
            },
        ),
        migrations.AddConstraint(
            model_name='subagreementtracking',
            constraint=models.CheckConstraint(check=models.Q(('PeriodOfPerformanceStart__lte', models.F('PeriodOfPerformanceEnd'))), name='PeriodOfPerfstart_lt_PeriodOfPerfEnd'),
        ),
        migrations.AddConstraint(
            model_name='subagreementtracking',
            constraint=models.CheckConstraint(check=models.Q(('EstimatedPeriodOfPerformanceStart__lte', models.F('EstimatedPeriodOfPerformanceEnd'))), name='EtdPeriodOfPerfst_lt_EtdPeriodOfPerfEnd'),
        ),
        migrations.AddConstraint(
            model_name='subagreementtracking',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('ParentAmendmentId__isnull', True), ('ParentRecord', True)), models.Q(('ParentAmendmentId__isnull', False), ('ParentRecord', False)), _connector='OR'), name='ParentAmendmentIsNullforParentRecord'),
        ),
    ]
