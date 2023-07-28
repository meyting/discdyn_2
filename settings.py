from os import environ

SESSION_CONFIGS = [
    dict(
         name='worker_sequences1',
         app_sequence=['sequences_before_worker'],
         num_demo_participants=10,
     ),
    dict(
         name='worker_alles',
         app_sequence=['instructions_worker', 'sequences_instructions', 'sequences_before_worker', 'treatment_info_worker', 'sequences_main_worker','survey_worker'],
         num_demo_participants=10,
     ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ["pairs", "usedprofiles", 'task_rounds', 'expiry', 'expiry_training', 'expiry_dropout1', 'total_points_sequence_training',
                      'uniqueID', 'id_worker', 'decision_pair', 'wrong_profile',
                      'total_points_sequence', 'bonus_sequences_before', 'target_sequences_before',
                      "sequences_sequence", "solutions_sequence",
                      "total_points_seq_main", 'bonus_sequences_main', 'target_sequences_main',
                      "sequences_main", "solutions_seq_main", "profile_participant", "exit_option", "time_exceeded",
                      "total_time", "start_time", "bonus_pre_hiring", "num_hirings_pc", "num_nothired_pc", "num_hirings",
                      "num_nothired"]
SESSION_FIELDS = ["used_labels", "free_labels"]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '8706067051652'
