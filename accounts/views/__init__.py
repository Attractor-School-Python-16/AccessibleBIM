from accounts.views.register_view import RegisterView, MySocialAccountAdapter
from accounts.views.profile_view import ProfileView
from accounts.views.password_update_view import PasswordUpdateView
from accounts.views.password_update_done_view import PasswordUpdateDoneView
from accounts.views.email_verification import InvalidVerificationLinkView, VerificationEmailSentView, \
    VerificationEmailNotSentView
from accounts.views.reset_password import ResetPasswordCompleteView, ResetPasswordConfirmView, ResetPasswordDoneView, \
    ResetPasswordView
from accounts.views.grant_moderator import GrantModeratorPanelView
