from controllers.v1.analytics_controller import AnalyticsController
from controllers.v1.auth_controller import AuthController
from controllers.v1.channel_admin_controller import ChannelAdminController
from controllers.v1.faq_controller import FaqController
from controllers.v1.message_controller import MessageController
from controllers.v1.admin_controller import AdminController
from controllers.v1.course_controller import CourseController
from controllers.v1.notification_controller import NotificationController
from controllers.v2.auth_controller import AuthController as AuthControllerV2
from controllers.v1.section_controller import SectionController
from controllers.v1.user_controller import UserController
from controllers.v1.exercise_controller import ExerciseController
from controllers.v1.balance_controller import BalanceController
from sanic import Sanic


def add_routes(app: Sanic):

    app.add_route(uri='/api/v1/auth/otp', handler=AuthController.otp, methods=['POST'])
    app.add_route(uri='/api/v1/analytics/install', handler=AnalyticsController.add_install, methods=['POST'])
    app.add_route(uri='/api/v1/check', handler=UserController.check_for_update, methods=['POST'])
    app.add_route(uri='/api/v1/auth/confirm', handler=AuthController.confirm, methods=['POST'])

    app.add_route(uri='/api/v2/auth/signup', handler=AuthControllerV2.signup, methods=['POST'])
    app.add_route(uri='/api/v2/auth/login', handler=AuthControllerV2.login, methods=['POST'])
    app.add_route(uri='/api/v2/auth/reset_password', handler=AuthControllerV2.update_password_request, methods=['POST'])
    app.add_route(uri='/api/v2/auth/reset_password', handler=AuthControllerV2.update_password, methods=['PUT'])

    app.add_route(uri='/api/v1/auth/refresh', handler=AuthController.refresh_token, methods=['GET'])
    app.add_route(uri='/api/v1/auth/unsub', handler=AuthController.refresh_token, methods=['POST'])

    app.add_route(uri='/api/v1/faq', handler=FaqController.get_all_faqs_user, methods=['GET'])
    app.add_route(uri='/api/v1/faq/<faq_id:uuid>', handler=FaqController.delete_faq, methods=['DELETE'])

    app.add_route(uri='/api/v1/profile', handler=UserController.get_user_profile, methods=['GET'])
    app.add_route(uri='/api/v1/profile/surename', handler=UserController.set_user_sure_name, methods=['POST'])
    app.add_route(uri='/api/v1/profile/firebase', handler=UserController.set_user_firebase_token, methods=['POST'])

    app.add_route(uri='/api/v1/message', handler=MessageController.get_all_messages, methods=['GET'])
    app.add_route(uri='/api/v1/message', handler=MessageController.send_message, methods=['POST'])
    app.add_route(uri='/api/v1/message/<message_id:uuid>', handler=MessageController.delete_message, methods=['DELETE'])

    app.add_route(uri='/api/v1/course', handler=CourseController.get_all_courses_user, methods=['GET'])

    app.add_route(uri='/api/v1/exercise', handler=ExerciseController.get_user_exercise, methods=['GET'])
    app.add_route(uri='/api/v1/exercise', handler=ExerciseController.add_user_exercise, methods=['POST'])
    app.add_route(uri='/api/v1/exercise/<exercise_id:uuid>/response', handler=ExerciseController.add_response, methods=['POST'])

    app.add_route(uri='/api/v1/course/<course_id:uuid>/buy', handler=CourseController.buy_course, methods=['POST'])
    app.add_route(uri='/api/v1/course/<course_id:uuid>/topics', handler=CourseController.get_course_topics, methods=['GET'])
    app.add_route(uri='/api/v1/course/<course_id:uuid>/faq', handler=CourseController.get_course_faqs, methods=['GET'])
    app.add_route(uri='/api/v1/course/<course_id:uuid>/question', handler=CourseController.get_course_questions, methods=['GET'])

    app.add_route(uri='/api/v1/payment/verify', handler=CourseController.verify_payment, methods=['POST'])

    # Admin section

    app.add_route(uri='/api/v1/admin/signup', handler=AdminController.created_user, methods=['POST'])
    app.add_route(uri='/api/v1/admin/login', handler=AdminController.login, methods=['POST'])

    app.add_route(uri='/api/v1/admin/faq', handler=FaqController.create_new_faq, methods=['POST'])
    app.add_route(uri='/api/v1/admin/faq', handler=FaqController.get_all_faqs, methods=['GET'])
    app.add_route(uri='/api/v1/admin/faq/<faq_id:uuid>', handler=FaqController.delete_faq, methods=['DELETE'])
    app.add_route(uri='/api/v1/admin/faq/<faq_id:uuid>', handler=FaqController.update_faq, methods=['PUT'])

    app.add_route(uri='/api/v1/admin/message', handler=MessageController.get_all_messages_admin, methods=['GET'])

    app.add_route(uri='/api/v1/admin/message/<message_id:uuid>', handler=MessageController.get_message_by_id, methods=['GET'])
    app.add_route(uri='/api/v1/admin/message/<message_id:uuid>/response', handler=MessageController.response_message, methods=['POST'])

    app.add_route(uri='/api/v1/admin/course', handler=CourseController.insert_new_course, methods=['POST'])
    app.add_route(uri='/api/v1/admin/course', handler=CourseController.get_all_courses, methods=['GET'])
    app.add_route(uri='/api/v1/admin/course/<course_id:uuid>', handler=CourseController.get_course_by_id, methods=['GET'])
    app.add_route(uri='/api/v1/admin/course/<course_id:uuid>', handler=CourseController.delete_course, methods=['DELETE'])
    app.add_route(uri='/api/v1/admin/course/<course_id:uuid>', handler=CourseController.update_course, methods=['PUT'])
    app.add_route(uri='/api/v1/admin/course/<course_id:uuid>/section', handler=SectionController.get_course_sections, methods=['GET'])

    app.add_route(uri='/api/v1/admin/section', handler=SectionController.insert_new_section, methods=['POST'])
    app.add_route(uri='/api/v1/admin/section/<section_id:uuid>', handler=SectionController.delete_section, methods=['DELETE'])
    app.add_route(uri='/api/v1/admin/section/<section_id:uuid>', handler=SectionController.update_section, methods=['PUT'])
    app.add_route(uri='/api/v1/admin/section/<section_id:uuid>', handler=SectionController.get_section_by_id, methods=['GET'])

    app.add_route(uri='/api/v1/admin/transaction', handler=UserController.get_all_transactions, methods=['GET'])
    app.add_route(uri='/api/v1/admin/user', handler=UserController.get_all_users, methods=['GET'])
    app.add_route(uri='/api/v1/admin/user/<user_id:uuid>/transaction', handler=UserController.get_user_transaction, methods=['GET'])

    app.add_route(uri='/api/v1/admin/exercise', handler=ExerciseController.get_all, methods=['GET'])
    app.add_route(uri='/api/v1/admin/exercise', handler=ExerciseController.add_exercise, methods=['POST'])
    app.add_route(uri='/api/v1/admin/exercise/<exercise_id:uuid>', handler=ExerciseController.delete_exercise, methods=['DELETE'])
    app.add_route(uri='/api/v1/admin/exercise/<exercise_id:uuid>', handler=ExerciseController.update_exercise, methods=['PUT'])

    app.add_route(uri='/api/v1/admin/section/<section_id:uuid>/exercise', handler=ExerciseController.get_by_section, methods=['GET'])
    app.add_route(uri='/api/v1/admin/course/<course_id:uuid>/exercise', handler=ExerciseController.get_by_course, methods=['GET'])
    app.add_route(uri='/api/v1/admin/channeladmin', handler=ChannelAdminController.get_all_channel_admins, methods=['GET'])
    app.add_route(uri='/api/v1/admin/channeladmin/<channel_admin_id:uuid>/distribution', handler=ChannelAdminController.get_channel_admin_distribution, methods=['GET'])
    app.add_route(uri='/api/v1/admin/channeladmin/<channel_admin_id:uuid>/recoupment', handler=ChannelAdminController.get_recoupment_account, methods=['GET'])
    app.add_route(uri='/api/v1/admin/channeladmin/<channel_admin_id:uuid>/new_password', handler=ChannelAdminController.admin_reset_password, methods=['GET'])

    app.add_route(uri='/api/v1/admin/update', handler=AdminController.add_new_app_version, methods=['POST'])
    app.add_route(uri='/api/v1/admin/channeladmin/<channel_admin_id:uuid>/status', handler=ChannelAdminController.set_channel_admin_status, methods=['PUT'])
    app.add_route(uri='/api/v1/admin/distribution/<distribution_id:uuid>/status', handler=ChannelAdminController.update_distribution_status, methods=['PUT'])

    app.add_route(uri='/api/v1/admin/balance', handler=BalanceController.add_balance, methods=['POST'])
    app.add_route(uri='/api/v1/admin/channeladmin/<channel_admin_id:uuid>/balance', handler=BalanceController.get_balance_by_channel_admin_id, methods=['GET'])

    app.add_route(uri='/api/v1/admin/notification', handler=NotificationController.add_new_notification, methods=['POST'])
    app.add_route(uri='/api/v1/admin/notification', handler=NotificationController.get_all_notifications, methods=['GET'])
    app.add_route(uri='/api/v1/admin/notification/<notification_id:uuid>', handler=NotificationController.get_by_id, methods=['GET'])


    # Channel Admin
    app.add_route(uri='/api/v1/channeladmin/auth/signup', handler=ChannelAdminController.create_new_admin, methods=['POST'])
    app.add_route(uri='/api/v1/channeladmin/auth/login', handler=ChannelAdminController.login, methods=['POST'])
    app.add_route(uri='/api/v1/channeladmin/profile', handler=ChannelAdminController.update_channel_account, methods=['PUT'])
    app.add_route(uri='/api/v1/channeladmin/channel', handler=ChannelAdminController.add_channel, methods=['POST'])
    app.add_route(uri='/api/v1/channeladmin/channel', handler=ChannelAdminController.get_channel_by_owner, methods=['GET'])
    app.add_route(uri='/api/v1/channeladmin/channel/<distribution_id:uuid>/transaction', handler=ChannelAdminController.get_distribution_transactions, methods=['GET'])
    app.add_route(uri='/api/v1/channeladmin/transactions', handler=ChannelAdminController.get_channel_admin_transactions, methods=['GET'])
    app.add_route(uri='/api/v1/channeladmin/app', handler=ChannelAdminController.get_distribution_app, methods=['GET'])

    app.add_route(uri='/api/v1/channeladmin/profile', handler=ChannelAdminController.get_channel_admin_profile, methods=['GET'])
    app.add_route(uri='/api/v1/channeladmin/balance', handler=ChannelAdminController.get_balances, methods=['GET'])
    app.add_route(uri='/api/v1/channeladmin/reset_password', handler=ChannelAdminController.channel_admin_reset_password, methods=['POST'])

    public_urls = [
        '/api/v1/auth/otp',
        '/api/v1/auth/confirm',
        '/api/v2/auth/signup',
        '/api/v2/auth/login',
        '/api/v2/auth/reset_password',
        '/api/v1/auth/refresh',
        '/api/v1/check',
        '/api/v1/channeladmin/auth/signup',
        '/api/v1/channeladmin/auth/login',
        '/api/v1/admin/signup',
        '/api/v1/admin/login',
        '/api/v1/admin/update',
        '/api/v1/analytics/install',
        '/api/v1/payment/verify'
    ]

    return public_urls
