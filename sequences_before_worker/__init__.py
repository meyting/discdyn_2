from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'sequences_before_worker'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 50
    TIMER_TEXT = "Remaining time for this task:"
    SEQUENCES_sequence = ['1 , 5 , 4 , 8 , 7 , ', '12 , 23 , 34 , 45 , ', '15 , 12 , 9 , 6 , ',
                          '2 , 6 , 4 , 12 , 10 , 30 , ',
                          '100 , 99 , 104 , 103 , 108 , ', '2 , 8 , 14 , 20 , ', '64 , 56 , 48 , 40 , ',
                          '2 , 5 , 4 , 7 , 6 , ', '120 , 120 , 60 , 20 , ', '1 , 9 , 2 , 99 , 3 , 999 , 4 , 9999 , ',
                          '8 , 13 , 18 , 23 , ', '2 , 6 , 10 , 14 , ', '18 , 36 , 72 , 144 , ', '7 , 17 , 27 , 37 , ',
                          '10 , 15 , 13 , 18 , ', '12 , 10 , 13 , 11 , 14 , ', '1 , 4 , 9 , 16 , 25 , ',
                          '24 , 34 , 44 , 54 , ',
                          '176 , 88 , 44 , 22 , ', '22 , 11 , 44 , 22 , 88 , ', '18 , 14 , 10 , 6 , ',
                          '1 , 1 , 2 , 3 , 5 , 8 , 13 , ', '124 , 62 , 64 , 32 , 34 , ', '2 , 4 , 6 , 8 , ',
                          '13 , 4 , 26 , 8 , 39 , ', '21 , 20 , 18 , 15 , 11 , ', '4 , 12 , 6 , 18 , 9 , ',
                          '1 , 1 , 2 , 6 , 24 , ', '50 , 40 , 31 , 23 , 16 , ', '10 , 11 , 13 , 16 , 20 , ',
                          '1 , 3 , 4 , 6 , 7 , ', '53 , 8 , 54 , 9 , 55 , 10 , ', '2 , 4 , 3 , 9 , 4 , 16 , ',
                          '27 , 23 , 19 , 15 , ', '10 , 18 , 26 , 34 , ', '101 , 91 , 81 , 71 , ',
                          '95 , 59 , 85 , 58 , 75 , ', '3 , 7 , 11 , 15 , 19 , ', '3 , 4 , 7 , 11 , 18 , ',
                          '9 , 15 , 21 , 27 , ', '9 , 18 , 27 , 36 , ',
                          '96 , 48 , 24 , 12 , ', '1 , 3 , 5 , 7 , ', '2  , 4  , 8  , 16  , ', '1 , 2 , 4 , 7 , 11 , ',
                          '1 , 3 , 9 , 27 , ', '32 , 26 , 20 , 14 , ', '11 , 22 , 33 , 44 , ', '10 , 15 , 20 , 25 , ',
                          '1 , 8 , 27 , 64 , ']
    SOLUTIONS_sequence = [11, 56, 3, 28, 107, 26, 32, 9, 5, 5, 28, 18, 288, 47, 16, 12, 36, 64, 11, 44, 2, 21, 17, 10,
                          12, 6, 27, 120, 10, 25, 9, 56, 5, 11, 42, 61, 57, 23, 29, 33, 45, 6, 9, 32, 16, 81, 8, 55, 30,
                          125, ]
    time_sequence = 300
    time_sequence_mins = round(time_sequence / 60)
    bonusfactor = cu(0.05)
    bonusexample_competition = 20
    bonusexample_comp_bonus = bonusexample_competition * bonusfactor


class Subsession(BaseSubsession):
    question_sequence = models.StringField()
    result_sequence = models.IntegerField()


def creating_session(subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.total_points_sequence = 0
            solutions_sequence = C.SOLUTIONS_sequence.copy()
            # random.Random(0).shuffle(solutions_sequence)
            solutions_sequence.extend(solutions_sequence)
            p.participant.solutions_sequence = solutions_sequence
            sequences_sequence = C.SEQUENCES_sequence.copy()
            # random.Random(0).shuffle(sequences_sequence)
            sequences_sequence.extend(sequences_sequence)
            p.participant.sequences_sequence = sequences_sequence
    for p in subsession.get_players():
        subsession.question_sequence = p.participant.sequences_sequence[p.round_number - 1]
        subsession.result_sequence = p.participant.solutions_sequence[p.round_number - 1]
        p.solution_sequence = subsession.result_sequence


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    input_sequence = models.IntegerField(label='', blank=True)
    solution_sequence = models.IntegerField()
    points_per_q_sequence = models.IntegerField(initial=0)
    total_points_sequence = models.IntegerField(initial=0)
    bonus_sequences_before = models.CurrencyField(initial=0)
    question_num_sequence = models.IntegerField(initial=0)


def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()


# PAGES

class StartLogic(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time
        participant.expiry = time.time() + C.time_sequence
        player.total_points_sequence = 0


class QuestionsLogic(Page):
    form_model = 'player'
    form_fields = ['input_sequence']
    get_timeout_seconds = get_timeout_seconds
    timer_text = C.TIMER_TEXT

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        player.question_num_sequence = player.round_number

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.field_maybe_none('input_sequence') == player.solution_sequence:
            player.points_per_q_sequence += 1
        participant = player.participant
        if player.field_maybe_none('input_sequence') == player.solution_sequence:
            participant.total_points_sequence += 1
        player.total_points_sequence = participant.total_points_sequence
        if player.total_points_sequence >= participant.target_sequences_before:
            participant.bonus_sequences_before = participant.target_sequences_before * C.bonusfactor
        else:
            participant.bonus_sequences_before = cu(0)
        player.bonus_sequences_before = participant.bonus_sequences_before
        # print ("bonus_sequences_before", participant.bonus_sequences_before)
        return player.total_points_sequence

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        # return player.round_number <= C.num_rounds_task and get_timeout_seconds(player) > 1
        return get_timeout_seconds(player) > 1


page_sequence = [StartLogic, QuestionsLogic]
