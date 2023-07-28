from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'sequences_instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    TIMER_TEXT = "Remaining time for this task:"
    SEQUENCES_training1 = '6 , 12 , 24 , 48 , '
    SEQUENCES_training2 = '3 , 8 , 7 , 12 , '
    SEQUENCES_training3 = '54 , 45 , 36 , 27 , '
    SOLUTIONS_training1 = 96
    SOLUTIONS_training2 = 11
    SOLUTIONS_training3 = 18
    time_sequences_training = 60
    time_sequences_training_min = time_sequences_training / 60
    num_sequences_training = 3
    num_sequences_task = 50
    time_sequence = 300
    time_sequence_mins = round(time_sequence / 60)
    bonusfactor = cu(0.05) #or 0.1?
    bonusexample1 = 10
    bonusexample2 = 40
    bonusexample1_comp_bonus = bonusexample1 * bonusfactor
    bonusexample2_comp_bonus = bonusexample2 * bonusfactor
    competition_bonusfactor = cu(0.1)



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    input_sequences_training = models.IntegerField(label='', blank=True)
    # solution_sequence_training = models.IntegerField()
    total_points_sequence_training = models.IntegerField(initial=0)
    target_sequences_before = models.IntegerField(label='')


def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry_training - time.time()


# PAGES
class InstructionsTask(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        import time
        participant = player.participant
        participant.expiry_training = time.time() + C.time_sequences_training
        participant.total_points_sequence_training = 0


# slider test
class TestSlider2(Page):
    form_model = 'player'
    form_fields = ['target_sequences_before', ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.num_sequences_training

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.target_sequences_before = player.target_sequences_before
        return participant.target_sequences_before

class TrainingSequences(Page):
    form_model = 'player'
    form_fields = ['input_sequences_training']
    get_timeout_seconds = get_timeout_seconds
    timer_text = C.TIMER_TEXT

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if player.round_number == 1:
            if player.field_maybe_none('input_sequences_training') == C.SOLUTIONS_training1:
                participant.total_points_sequence_training += 1
                # player.total_points_sequence_training += 1
        if player.round_number == 2:
            if player.field_maybe_none('input_sequences_training') == C.SOLUTIONS_training2:
                participant.total_points_sequence_training += 1
                # player.total_points_sequence_training += 1
        if player.round_number == 3:
            if player.field_maybe_none('input_sequences_training') == C.SOLUTIONS_training3:
                participant.total_points_sequence_training += 1
        player.total_points_sequence_training = participant.total_points_sequence_training
        return player.total_points_sequence_training

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        # return player.round_number <= C.num_rounds_task and get_timeout_seconds(player) > 1
        return get_timeout_seconds(player) > 1


class ResultsTraining(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.num_sequences_training


#class InstructionsPayment(Page):
#    form_model = 'player'
#    form_fields = ['target_sequences_before', ]

#    @staticmethod
#    def is_displayed(player: Player):
#        return player.round_number == C.num_sequences_training

#    @staticmethod
#    def before_next_page(player: Player, timeout_happened):
#        participant = player.participant
#        participant.target_sequences_before = player.target_sequences_before
#        print("VVVVVVVVVVVVV", participant.target_sequences_before)
#        return participant.target_sequences_before


page_sequence = [InstructionsTask, TrainingSequences, ResultsTraining, TestSlider2]
