from otree.api import *

import time

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey_worker'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    num_employers = 10 # number of employers (decisions) per pair
    time_survey = 480
    time_decisions = 300 # for no info treatment
    TIMER_TEXT = "To be not excluded from the experiment due to inactivity, please continue with the next page within:"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    hiring_decision_pro = models.StringField(verbose_name='')
    hiring_decision_con = models.StringField(verbose_name='')
    hiring_decision_pro_pc = models.StringField(verbose_name='')
    hiring_decision_con_pc = models.StringField(verbose_name='')
    total_bonus_seq = models.FloatField(initial=0)
    education = models.CharField(initial=None,
                                 verbose_name='What is your highest achieved level of education?',
                                 choices=['Did not graduate high school', 'High school or GED',
                                          'Began college, no degree yet', 'Bachelor', 'Associate', 'Master',
                                          'Doctoral', 'other'], )
    party = models.CharField(initial=None,
                             verbose_name='In politics today, do you consider yourself a Republican, a Democrat , or an Independent?',
                             choices=['Republican', 'Democrat', 'Independent'], )
    purpose = models.LongStringField(initial=None,
                                     blank=True,
                                     verbose_name="What do you think this experiment is about?")
    discrimination = models.LongStringField(initial=None,
                                 blank=True,
                                 verbose_name="Have you experienced discrimination in the past?")
    reason_hiring = models.LongStringField(initial=None,
                                            blank=True,
                                            verbose_name="What do you think was the main reason for the employers to decide who to hire?")
    risk_aversion = models.IntegerField(
        widget=widgets.RadioSelect, choices=[['1','...strongly dislike risks.'], ['2','...rather avoid risks.'], ['3','...am neutral.'],
                                                 ['4', '...rather like risks.'], ['5','...strongly like risks.']],
        label='',
    )
    competition_aversion = models.IntegerField(
        widget=widgets.RadioSelect, choices=[['1','...strongly dislike competitions.'], ['2', '...rather avoid competitions.'],
                                                 ['3', '...am neutral.'],
                                                 ['4', '...rather like competitions.'], ['5', '...strongly like competitions.']],
    )
    gpa_hs = models.FloatField(initial=None, blank=True,
                               verbose_name='What is your final (or current) high school GPA?')
    gpa_college = models.FloatField(initial=None, blank=True,
                                    verbose_name='What is your final (or current) college GPA?')


class EmployerDecisions(Page):
    form_model = 'player'
    timeout_seconds = C.time_decisions
    timer_text = C.TIMER_TEXT

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        """
        worker1_id = participant.decision_pair["worker_id"]
        worker1_gender = participant.decision_pair["gender"]
        worker1_race = participant.decision_pair['race']
        worker1_agegroup = participant.decision_pair['agegroup']
        worker2_id = participant.decision_pair['opponent_id']
        worker2_gender = participant.decision_pair['gender_opp']
        worker2_race = participant.decision_pair['race_opp']
        worker2_agegroup = participant.decision_pair['agegroup_opp']
        """
        hiring_decision_pro = player.participant.decision_pair['decisions_pro']
        hiring_decision_pro_pc = hiring_decision_pro*10
        hiring_decision_con = player.participant.decision_pair['decisions_con']
        hiring_decision_con_pc = hiring_decision_con*10
        treatment = participant.decision_pair['treatment']
        bonus_pre_hiring = participant.bonus_pre_hiring
        return {'hiring_decision_pro': hiring_decision_pro,
                'hiring_decision_con': hiring_decision_con,
                'hiring_decision_pro_pc': hiring_decision_pro_pc,
                'hiring_decision_con_pc': hiring_decision_con_pc,
                'treatment': treatment,
                'bonus_pre_hiring': bonus_pre_hiring,
                }

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.decision_pair['treatment'] == 3

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        session = player.session
        if timeout_happened:
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['education', 'party', 'purpose', 'discrimination', 'reason_hiring', 'risk_aversion', 'competition_aversion',
                   'gpa_hs', 'gpa_college',]
    timeout_seconds = C.time_survey
    timer_text = C.TIMER_TEXT


class ResultsWorker(Page):
    def vars_for_template(player: Player):
        participant = player.participant
        exit_option = participant.exit_option
        bonus_pre_hiring = participant.bonus_pre_hiring
        total_bonus_seq = participant.vars['bonus_sequences_before'] + participant.vars['bonus_sequences_main'] + bonus_pre_hiring
        return {
            'total_points_sequence': participant.vars['total_points_sequence'],
            'target_sequences_before': participant.vars['target_sequences_before'],
            'bonus_sequences_before': participant.vars['bonus_sequences_before'],
            'total_points_seq_main': participant.vars['total_points_seq_main'],
            'target_sequences_main': participant.vars['target_sequences_main'],
            'bonus_sequences_main': participant.vars['bonus_sequences_main'],
            'total_bonus_seq': total_bonus_seq,
            'bonus_pre_hiring': bonus_pre_hiring,
            'exit_option': exit_option,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        session = player.session
        if timeout_happened:
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")


page_sequence = [EmployerDecisions, Survey, ResultsWorker]
