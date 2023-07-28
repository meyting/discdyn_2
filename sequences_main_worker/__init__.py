from otree.api import *


doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'sequences_main_worker'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 50
    TIMER_TEXT = "Remaining time for this task:"
    SEQUENCES_main = ['0 , 1 , 3 , 6 , 10 , ', '10 , 20 , 30 , 40 , ', '000 , 001 , 010 , 011 , ', '9 , 13 , 17 , 21 , ',
                      '16 , 14 , 12 , 10 , ', '2 , 3 , 5 , 7 , 11 , 13 , ', '66 , 61 , 56 , 51 , ', '2 , 6 , 12 , 20 , ',
                      '1 , 3 , 4 , 6 , 7 , ', '4 , 15 , 26 , 37 , ', '5 , 10 , 20 , 40 , ', '11 , 2 , 22 , 4 , 33 , ',
                      '2 , 4 , 6 , 10 , 16 , ', '24 , 21 , 18 , 15 , ',  '0 , 5 , 15 , 30 , ', '8 , 10 , 7 , 9 , ',
                      '8 , 15 , 22 , 29 , ', '1 , 11 , 2 , 22 , 3 , ', '2 , 6 , 4 , 12 , 10 , ', '0 , 4 , 16 , 36 , ',
                      '8 , 16 , 24 , 32 , ', '87 , 77 , 67 , 57 , ', '64 , 32 , 16 , 8 , ', '2 , 12 , 6 , 16 , 8 , ',
                      '10 , 20 , 40 , 80 , ', '13 , 26 , 39 , 52 , ', '40 , 31 , 22 , 13 , ', '100 , 50 , 60 , 30 , 40',
                      '19 , 17 , 15 , 13 , ', '4 , 24 , 44 , 64 , ', '9 , 16 , 25 , 36 , ', '10 , 1 , 11 , 2 , 12 , ',
                      '2 , 8 , 4 , 16 , 12 , ', '123 , 234 , 345 , 456 , ', '6 , 7 , 9 , 12 , 16 , ', '9999 , 8 , 999 , 7 , 99 , ',
                      '100 , 89 , 78 , 67 , ', '6 , 12 , 18 , 24 , ', '0 , 3 , 3 , 6 , 9 , 15 , ', '50 , 45 , 40 , 35 , ',
                      '3 , 33 , 63 , 93 , ', '0 , 4 , 1 , 5 , 2, ', '55 , 10 , 44 , 8 , 33 , ', '80 , 64 , 48 , 32 , ',
                      '2 , 4 , 3 , 9 , 8 , ', '7 , 10 , 13 , 16 , ', '20 , 19 , 17 , 14 , 10 , ', '1 , 2 , 6 , 12 , 36,  ',
                      '10000, 1000 , 100 , ', '1 , 17 , 1 , 17 , 1 , ',]
    SOLUTIONS_seq_main = [15, 50, 100, 25, 8, 17, 46, 30, 9, 48, 80, 6, 26, 12, 50, 6, 36, 33, 30, 64, #20
                          40, 47, 4, 18, 160, 65, 4, 20, 11, 84, 49, 3, 48, 567, 21, 6, 56, 30, 24, 30,   #40
                        123, 6, 6, 16, 64, 19, 5, 72, 10, 17]
    time_sequence = 300
    time_sequence_mins = round(time_sequence / 60)
    number_employers = 10
    # compensation_exit = cu(0.2)
    bonusfactor = cu(0.05)
    bonusexample_competition = 20
    bonusexample_comp_bonus = bonusexample_competition * bonusfactor
    bonushired = cu(1)
    bonus_threshold = 5
    time_instructions_seq = 300
    TIMER_TEXT_dropout = "To not be excluded from the experiment due to inactivity, please continue with the next page within:"


class Subsession(BaseSubsession):
    question_seq_main = models.StringField()
    result_seq_main = models.IntegerField()


def creating_session(subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.total_points_seq_main = 0
            solutions_seq_main = C.SOLUTIONS_seq_main.copy()
            solutions_seq_main.extend(solutions_seq_main)
            p.participant.solutions_seq_main = solutions_seq_main
            sequences_main = C.SEQUENCES_main.copy()
            sequences_main.extend(sequences_main)
            p.participant.sequences_main = sequences_main
    for p in subsession.get_players():
        subsession.question_seq_main = p.participant.sequences_main[p.round_number - 1]
        subsession.result_seq_main = p.participant.solutions_seq_main[p.round_number - 1]
        p.solution_seq_main = subsession.result_seq_main


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    input_seq_main = models.IntegerField(label='', blank=True)
    solution_seq_main = models.IntegerField()
    points_per_q_seq_main = models.IntegerField(initial=0)
    total_points_seq_main = models.IntegerField(initial=0)
    question_num_seq_main = models.IntegerField(initial=0)
    target_sequences_main = models.IntegerField(label='')
    bonus_sequences_main = models.CurrencyField(initial=0)
    exit_option = models.StringField(choices=[['continue', 'participate in the hiring round'],
                                              ['no_hiring', 'not participate in the hiring round'],],
                                     widget=widgets.RadioSelect, verbose_name='What do you want to do?')


def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()


# PAGES
class InstructionsPart2(Page):
    form_model = 'player'
    # form_fields = ['exit_option']
    timeout_seconds = C.time_instructions_seq
    timer_text = C.TIMER_TEXT_dropout

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        session = player.session
        if timeout_happened:
            print("timeout happened")
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")




class TestSlider2(Page):
    form_model = 'player'
    form_fields = ['target_sequences_main', ]
    timeout_seconds = C.time_instructions_seq
    timer_text = C.TIMER_TEXT_dropout

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == 1

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.target_sequences_main = player.target_sequences_main
        session = player.session
        if timeout_happened:
            print("timeout happened")
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")
        return participant.target_sequences_main

#class SequencesPaymentMain(Page):
#    form_model = 'player'
#    form_fields = ['target_sequences_main']
#    timeout_seconds = C.time_instructions_seq
#    timer_text = C.TIMER_TEXT_dropout

#    @staticmethod
#    def is_displayed(player: Player):
#        participant = player.participant
#        return player.round_number == 1


class StartLogic(Page):
    timeout_seconds = C.time_instructions_seq
    timer_text = C.TIMER_TEXT_dropout

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time
        # participant.exit_option = player.exit_option
        participant.expiry = time.time() + C.time_sequence
        player.total_points_seq_main = 0
        session = player.session
        if timeout_happened:
            print("timeout happened")
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")


class QuestionsLogic(Page):
    form_model = 'player'
    form_fields = ['input_seq_main']
    get_timeout_seconds = get_timeout_seconds
    timer_text = C.TIMER_TEXT

    @staticmethod
    def vars_for_template(player: Player):
        player.question_num_seq_main = player.round_number

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.field_maybe_none('input_seq_main') == player.solution_seq_main:
            player.points_per_q_seq_main += 1
        participant = player.participant
        if player.field_maybe_none('input_seq_main') == player.solution_seq_main:
            participant.total_points_seq_main += 1
        player.total_points_seq_main = participant.total_points_seq_main
        if player.total_points_seq_main >= participant.target_sequences_main:
            participant.bonus_sequences_main = participant.target_sequences_main * C.bonusfactor
        else:
            participant.bonus_sequences_main = cu(0)
        player.bonus_sequences_main = participant.bonus_sequences_main
        return player.total_points_seq_main

    @staticmethod
    def is_displayed(player: Player):
        return get_timeout_seconds(player) > 1


class ExitOption(Page):
    form_model = 'player'
    form_fields = ['exit_option']
    timeout_seconds = C.time_instructions_seq
    timer_text = C.TIMER_TEXT_dropout

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.exit_option = player.exit_option
        session = player.session
        if timeout_happened:
            print("timeout happened")
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == C.NUM_ROUNDS


page_sequence = [InstructionsPart2, TestSlider2,#SequencesPaymentMain,
                 StartLogic, QuestionsLogic, ExitOption]
