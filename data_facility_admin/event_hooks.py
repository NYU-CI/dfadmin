from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
import logging
import boto3
# import boto3.ClientError
import json
from django.conf import settings
import copy

logger = logging.getLogger(__name__)

SNS_HOOK = settings.SNS_HOOK


def send_sns_event(topic, subject, payload):
    logger.debug('[send_sns_event] Topic:%s, Subject:%s\nPayload:%s' % (topic, subject, payload))
    if SNS_HOOK['AWS_ACCESS_KEY_ID']:
        logger.debug('Authenticating with credentials from env')
        sns = boto3.client('sns',
                           region_name=SNS_HOOK['REGION'],
                           aws_access_key_id=SNS_HOOK['AWS_ACCESS_KEY_ID'],
                           aws_secret_access_key=SNS_HOOK['AWS_ACCESS_KEY'],
                           aws_session_token=SNS_HOOK['AWS_SESSION_TOKEN']
                           )
    else:
        # When running on AWS, instance roles should be used.
        logger.debug('Authenticating with IAM Role')
        sns = boto3.client('sns', region_name=SNS_HOOK['REGION'])

    response = sns.publish(
        TargetArn='%s:%s' % (SNS_HOOK['BASE_ARN'], topic),
        Subject=subject,
        Message=json.dumps({"default": json.dumps(payload)}),
        MessageStructure='json'
    )

    # response = sns.publish(
    #     TopicArn='arn:aws:sns:us-east-1:441870321480:adrf-dataset-created',
    #     Message='Hello World!',
    # )
    logger.debug('SNS Response: %s' % response)
    # except ClientError as error:
    #     raise
    logger.info('SNS Event pushed with success: %s - %s' % (topic, subject))


def dataset_saved(instance, **kwargs):
    if not SNS_HOOK['ACTIVE']: return
    from data_facility_admin.models import Dataset

    logger.debug('Dataset saved - instance: {0} params: {1}'.format(instance, kwargs))

    created = kwargs['created'] if 'created' in kwargs else instance.id is None
    # When added to an active project
    if created:
        topic = SNS_HOOK['TOPIC_DATASET_CREATED']
        subject = 'Dataset created: {0}'.format(instance.dataset_id)
    else:
        topic = SNS_HOOK['TOPIC_DATASET_UPDATED']
        subject = 'Dataset updated: {0}'.format(instance.dataset_id)

    payload = {
        'entity_id': instance.dataset_id,
        'url': settings.DFADMIN_URL + '/api/v1/datasets/{0}'.format(instance.dataset_id),
        'sender': 'DFAdmin',
        'status': instance.status,
        'entity': instance.name,
    }
    send_sns_event(topic, subject, payload)

    # Check event dataset activated
    logger.debug('Checking if the dataset was activated...')
    try:
        old_instance = Dataset.objects.get(id=instance.id)
    except Dataset.DoesNotExist:
        old_instance = None

    if instance.status == Dataset.STATUS_ACTIVE and (created or old_instance.status != instance.status):
            logger.debug('Dataset activated: %s' % instance.dataset_id)
            subject = 'Dataset activated: {0}'.format(instance.dataset_id)
            send_sns_event(SNS_HOOK['TOPIC_DATASET_ACTIVATED'], subject, payload)

    # Check for deactivation
    logger.debug('Checking if the dataset was deactivated...')
    if not created and instance.status != Dataset.STATUS_ACTIVE and old_instance.status == Dataset.STATUS_ACTIVE:
        logger.debug('Dataset activated: %s' % instance.dataset_id)
        subject = 'Dataset deactivated: {0}'.format(instance.dataset_id)
        send_sns_event(SNS_HOOK['TOPIC_DATASET_DEACTIVATED'], subject, payload)

    logger.debug('Checking for database schema updates...')
    current_schema = instance.database_schema
    old_schema = None if old_instance is None else old_instance.database_schema
    if current_schema is not None:
        if old_schema is None or old_schema != current_schema:
            logger.debug('Dataset DB schema activated: %s' % current_schema.name)
            subject = '{0} - {1}'.format(instance.dataset_id, current_schema.name)
            payload['extra'] = {'schema': current_schema.name}
            send_sns_event(SNS_HOOK['TOPIC_DATASET_DB_ACTIVATED'], subject, payload)

        if old_schema is not None:
            logger.debug('Dataset DB schema changed. Deactivate previous one: %s' % old_schema.name)
            subject = '{0} - {1}'.format(instance.dataset_id, old_schema.name)
            payload['extra'] = {'schema': old_schema.name}
            send_sns_event(SNS_HOOK['TOPIC_DATASET_DB_DEACTIVATED'], subject, payload)







