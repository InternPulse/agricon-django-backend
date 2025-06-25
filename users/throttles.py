from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# Throttle for unauthenticated (IP-based) OTP requests
class OTPRequestAnonThrottle(AnonRateThrottle):
    scope = 'otp_anon_request'

# Throttle for authenticated (User-ID-based) OTP requests
class OTPRequestUserThrottle(UserRateThrottle):
    scope = 'otp_user_request'

# Throttle for unauthenticated (IP-based) login attempts
class LoginAttemptAnonThrottle(AnonRateThrottle):
    scope = 'login_anon_attempt'

# Throttle for unauthenticated (IP-based) OTP verification attempts
class OTPVerifyAnonThrottle(AnonRateThrottle):
    scope = 'otp_verify_anon'

class SignupAnonThrottle(AnonRateThrottle):
    scope = 'signup_anon_request'