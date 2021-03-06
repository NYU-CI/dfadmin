from data_facility_admin.models import Project, ProjectMember, ProjectRole, User, ProjectTool
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
import logging
from . import rds_client

logger = logging.getLogger(__name__)


# @receiver(pre_save, sender=ProjectTool)
# def set_default_config_on_rds(sender, instande, **kwargs):
#     logger.debug('set_default_config_on_rds - from "{0}" with params: {1}, {2}'.format(sender, instance, kwargs))
#     project_tool = instance
#     project = project_tool.project
#     if project_tool.tool_name == ProjectTool.TOOL_CHOICES.PG_RDS and not project_tool.system_info:
#         logger.debug("Initializing system info")
#         project_tool.system_info = rds_client.DEFAULT_CONFIG
#         logger.debug("done.")


@receiver(post_save, sender=ProjectTool)
def project_tool_saved(sender, instance, **kwargs):
    logger.debug('project_tool_saved - from "{0}" with instance: {1} params: {2}'.format(sender, instance, kwargs))
    project_tool = instance
    project = project_tool.project
    if project_tool.tool_name == ProjectTool.TOOL_CHOICES.PG_RDS:
        logger.debug("RDS found for project '%s'" % project.ldap_name)
        logger.debug("Project.is_active=%s" % project.is_active())

        # When added to an active project
        if kwargs['created']:
            logger.info('RDS added for project: "%s"' % project.ldap_name)
            rds_client.create_database(project_tool)


@receiver(post_delete, sender=ProjectTool)
def project_tool_deleted(sender, instance, **kwargs):
    logger.debug('project_tool_deleted - from "{0}" with params: {1}'.format(sender, kwargs))
    project_tool = instance
    project = project_tool.project
    if project_tool.tool_name == ProjectTool.TOOL_CHOICES.PG_RDS:
        logger.debug("RDS found")
        rds_client.delete_database(project_tool)


@receiver(post_save, sender=ProjectMember)
def project_membership_saved(sender, instance, **kwargs):
    logger.debug('project_membership_saved')
    rds_client.grant_access(instance)

@receiver(post_delete, sender=ProjectMember)
def project_membership_deleted(sender, instance, **kwargs):
    logger.debug('project_membership_saved')
    rds_client.revoke_access(instance)

