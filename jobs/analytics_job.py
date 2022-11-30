# Updating each distribution statistics

from model.distribution_model import DistributionModel
from model.user_model import UserModel
from model.analytics_model import AnalyticsModel

import logging
import sys

logger = logging.getLogger("BUILDER_LOGGER")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


distributions = DistributionModel().get_all_active_sync()

for distribution in distributions:
    dist_id = distribution['id']
    total_users = UserModel().count_by_keyword_sync(dist_id)[0]['total_users']
    total_analytics = AnalyticsModel().get_installed_count(dist_id)[0]['total_install']

    updated = DistributionModel().update_analytics_sync(dist_id=dist_id, total_users=total_users, total_installed=total_analytics)
    logger.info("updated distribution {}".format(dist_id))