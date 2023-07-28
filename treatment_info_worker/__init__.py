from otree.api import *
import pandas as pd
import numpy as np


df1 = pd.read_excel('_static\global\worker_pairs_decision.xlsx', keep_default_na = False, engine = 'openpyxl')


class C(BaseConstants):
    NAME_IN_URL = 'treatment_info_worker'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    num_employers = 10
    num_decisions_pc = 10
    session = 6  # set session number according to the profile for which the session is created (1: male, white, 20-24 / 2: male, white, 25-29 / ... 5: male, black, 20-24)
    # (only thing that needs to be changed)
    """
    labels_alle_sessions = [['1a', '1b', '1a', '1b', '1a', '1b', '1a', '1b', '1a', '1b', ],
                            ['2a', '2b', '2a', '2b', '2a', '2b', '2a', '2b', '2a', '2b', ],
                            ['3a', '3b', '3a', '3b', '3a', '3b', '3a', '3b', '3a', '3b', ],
                            ['4a', '4b', '4a', '4b', '4a', '4b', '4a', '4b', '4a', '4b', ],
                            ['5a', '5b', '5a', '5b', '5a', '5b', '5a', '5b', '5a', '5b', ],
                            ['6a', '6b', '6a', '6b', '6a', '6b', '6a', '6b', '6a', '6b', ],
                            ['7a', '7b', '7a', '7b', '7a', '7b', '7a', '7b', '7a', '7b', ],
                            ['8a', '8b', '8a', '8b', '8a', '8b', '8a', '8b', '8a', '8b', ],
                            ['9a', '9b', '9a', '9b', '9a', '9b', '9a', '9b', '9a', '9b', ],
                            ['10a', '10b', '10a', '10b', '10a', '10b', '10a', '10b', '10a', '10b', ],
                            ['11a', '11b', '11a', '11b', '11a', '11b', '11a', '11b', '11a', '11b', ],
                            ['12a', '12b', '12a', '12b', '12a', '12b', '12a', '12b', '12a', '12b'],
                            ['13a', '13b', '13a', '13b', '13a', '13b', '13a', '13b', '13a', '13b', ],
                            ['14a', '14b', '14a', '14b', '14a', '14b', '14a', '14b', '14a', '14b', ],
                            ['15a', '15b', '15a', '15b', '15a', '15b', '15a', '15b', '15a', '15b', ],
                            ['16a', '16b', '16a', '16b', '16a', '16b', '16a', '16b', '16a', '16b', ],
                            ]
                            """
    labels_alle_sessions = [['1a', '1b'],
                            ['2a', '2b'],
                            ['3a', '3b'],
                            ['4a', '4b'],
                            ['5a', '5b'],
                            ['6a', '6b'],
                            ['7a', '7b'],
                            ['8a', '8b'],
                            ['9a', '9b'],
                            ['10a', '10b'],
                            ['11a', '11b'],
                            ['12a', '12b'],
                            ['13a', '13b'],
                            ['14a', '14b'],
                            ['15a', '15b'],
                            ['16a', '16b'],
                            ]
    time_treatment_page = 360
    TIMER_TEXT = "To be not excluded from the experiment due to inactivity, please continue with the next page within:"
    pre_threshold_bonus = 5
    pre_hiring_bonus = cu(0.5)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    session = subsession.session
    labels_this_session = C.labels_alle_sessions[C.session - 1]
    session.free_labels = []
    session.free_labels = labels_this_session
    import random
    random.shuffle(session.free_labels)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    worker1_id = models.StringField(verbose_name='')
    worker1_gender = models.StringField(verbose_name='')
    worker1_race = models.StringField(verbose_name='')
    worker1_agegroup = models.StringField(verbose_name='')
    worker2_id = models.StringField(verbose_name='')
    worker2_gender = models.StringField(verbose_name='')
    worker2_race = models.StringField(verbose_name='')
    worker2_agegroup = models.StringField(verbose_name='')
    hiring_decision_pro = models.StringField(verbose_name='')
    hiring_decision_con = models.StringField(verbose_name='')
    hiring_decision_pro_pc = models.StringField(verbose_name='')
    hiring_decision_con_pc = models.StringField(verbose_name='')
    treatment = models.StringField(verbose_name='')
    num_hirings = models.IntegerField(initial=0)
    num_hirings_pc = models.IntegerField(initial=0)
    num_nothired = models.IntegerField(initial=0)
    num_nothired_pc = models.IntegerField(initial=0)


"""
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()
"""


# PAGES
class InstructionsDecisions(Page):
    form_model = 'player'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time
        import random
        participant.expiry = time.time() + C.time_treatment_page  # start timer for treatment page (drop out-problem)
        k = C.session - 1
        session = player.session
        print ("list of free labels", session.free_labels)
        if not participant.wrong_profile:
            if len(session.free_labels) != 0:
                player.participant.label = random.choice(session.free_labels)
                session.used_labels.append(player.participant.label)
                session.free_labels.remove(player.participant.label)
                print ("list of free labels", session.free_labels)
            else:
                player.participant.label = random.choice(C.labels_alle_sessions[k])
        else:
            player.participant.label = "1a" # (die Leute sind eigentlich schon vorne rausgefiltert)
        """ old version: 
        if not participant.wrong_profile:
            if C.labels_alle_sessions[k][player.id_in_group - 1] not in session.used_labels:
                player.participant.label = C.labels_alle_sessions[k][player.id_in_group - 1]
                # evtl. change to corresponding session-profile-list to use random labels
                session.used_labels.append(player.participant.label)
                # add option to take other profile-label if that is not used yet (or "free_labels"-list)
            else: # sollte am besten nicht passieren
                player.participant.label = "1b"
            # change to something else... None?
            print ("list of used labels", session.used_labels)
        else:
            player.participant.label = "1a" #change for experiment to None or something (other experiment then --> passiert an der Stelle also gar nicht mehr)
            """
        i = df1[df1['IDWorker'] == player.participant.label].index[0] # gives row number of corresponding label in excel
        print(i)
        participant.decision_pair = {'worker_id': df1['IDWorker'][i],
                                     'gender': df1['gender'][i],
                                     'race': df1['race'][i],
                                     'agegroup': df1["agegroup"][i],
                                     'opponent_id': df1["IDOpponent"][i],
                                     'gender_opp': df1["genderOpp"][i],
                                     'race_opp': df1["raceOpp"][i],
                                     'agegroup_opp': df1["agegroupOpp"][i],
                                     'decisions_pro': df1["decisionspro"][i],
                                     'decisions_con': df1["decisionscon"][i],
                                     'treatment': df1["treatment"][i],
                                     }
        print("DECISION PAIR", participant.decision_pair)
        # new:
        if participant.decision_pair['treatment'] <= 3:
            if participant.decision_pair['decisions_pro'] > 5:
                participant.bonus_pre_hiring = C.pre_hiring_bonus
            elif participant.decision_pair['decisions_pro'] < 5:
                participant.bonus_pre_hiring = cu(0)
            else:
                participant.bonus_pre_hiring = random.choice([cu(0), C.pre_hiring_bonus])
        else:
            p_hired = 0.5
            draws = np.random.poisson(p_hired, size=10)
            participant.num_hirings = sum(draws)
            participant.num_nothired = 10 - participant.num_hirings
            participant.num_hirings_pc = participant.num_hirings * 10
            participant.num_nothired_pc = participant.num_nothired * 10
            if participant.num_hirings > 5:
                participant.bonus_pre_hiring = C.pre_hiring_bonus
            elif participant.num_hirings < 5:
                participant.bonus_pre_hiring = cu(0)
            elif participant.num_hirings == 5:
                participant.bonus_pre_hiring = np.random.choice([cu(0), C.pre_hiring_bonus])
            else:
                participant.bonus_pre_hiring = np.random.choice([cu(0), C.pre_hiring_bonus])
                print ("FAIL")
        print ("BONUS PRE HIRING", participant.bonus_pre_hiring)


class PairHiringDiscr(Page):
    form_model = 'player'
    form_fields = ['worker1_id', 'worker1_gender', 'worker1_race', 'worker1_agegroup',
                   'worker2_id', 'worker2_gender', 'worker2_race', 'worker2_agegroup',]
    # get_timeout_seconds = get_timeout_seconds
    timeout_seconds = C.time_treatment_page
    timer_text = C.TIMER_TEXT

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        worker1_id = participant.decision_pair["worker_id"]
        worker1_gender = participant.decision_pair["gender"]
        worker1_race = participant.decision_pair['race']
        worker1_agegroup = participant.decision_pair['agegroup']
        worker2_id = participant.decision_pair['opponent_id']
        worker2_gender = participant.decision_pair['gender_opp']
        worker2_race = participant.decision_pair['race_opp']
        worker2_agegroup = participant.decision_pair['agegroup_opp']
        hiring_decision_pro = player.participant.decision_pair['decisions_pro']
        # transform hiring_decision_pro in percentage:
        hiring_decision_pro_pc = hiring_decision_pro*10
        hiring_decision_con = player.participant.decision_pair['decisions_con']
        # transform hiring_decision_con in percentage:
        hiring_decision_con_pc = hiring_decision_con*10
        treatment = participant.decision_pair['treatment']
        # new:
        bonus_pre_hiring = participant.bonus_pre_hiring
        return {'worker1_id': worker1_id,
                'worker1_gender': worker1_gender,
                'worker1_race': worker1_race,
                'worker1_agegroup': worker1_agegroup,
                'worker2_id': worker2_id,
                'worker2_gender': worker2_gender,
                'worker2_race': worker2_race,
                'worker2_agegroup': worker2_agegroup,
                'hiring_decision_pro': hiring_decision_pro,
                'hiring_decision_con': hiring_decision_con,
                'hiring_decision_pro_pc': hiring_decision_pro_pc,
                'hiring_decision_con_pc': hiring_decision_con_pc,
                'treatment': treatment,
                # new:
                'bonus_pre_hiring': bonus_pre_hiring,
                }

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.decision_pair['treatment'] == 1 # and get_timeout_seconds(player) > 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        # if get_timeout_seconds(player) <= 0:
        if timeout_happened:
            print("timeout happened")
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")


class PairHiringNoDiscr(Page):
    form_model = 'player'
    form_fields = ['worker1_id', 'worker1_gender', 'worker1_race', 'worker1_agegroup',
                   'worker2_id', 'worker2_gender', 'worker2_race', 'worker2_agegroup',]
    # get_timeout_seconds = get_timeout_seconds
    timeout_seconds = C.time_treatment_page
    timer_text = C.TIMER_TEXT

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        worker1_id = participant.decision_pair["worker_id"]
        worker1_gender = participant.decision_pair["gender"]
        worker1_race = participant.decision_pair['race']
        worker1_agegroup = participant.decision_pair['agegroup']
        worker2_id = participant.decision_pair['opponent_id']
        worker2_gender = participant.decision_pair['gender_opp']
        worker2_race = participant.decision_pair['race_opp']
        worker2_agegroup = participant.decision_pair['agegroup_opp']
        hiring_decision_pro = player.participant.decision_pair['decisions_pro']
        # transform hiring_decision_pro in percentage:
        hiring_decision_pro_pc = hiring_decision_pro*10
        hiring_decision_con = player.participant.decision_pair['decisions_con']
        # transform hiring_decision_con in percentage:
        hiring_decision_con_pc = hiring_decision_con*10
        treatment = participant.decision_pair['treatment']
        bonus_pre_hiring = participant.bonus_pre_hiring
        return {'worker1_id': worker1_id,
                'worker1_gender': worker1_gender,
                'worker1_race': worker1_race,
                'worker1_agegroup': worker1_agegroup,
                'worker2_id': worker2_id,
                'worker2_gender': worker2_gender,
                'worker2_race': worker2_race,
                'worker2_agegroup': worker2_agegroup,
                'hiring_decision_pro': hiring_decision_pro,
                'hiring_decision_con': hiring_decision_con,
                'hiring_decision_pro_pc': hiring_decision_pro_pc,
                'hiring_decision_con_pc': hiring_decision_con_pc,
                'treatment': treatment,
                'bonus_pre_hiring': bonus_pre_hiring,
                }

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.decision_pair['treatment'] == 2 # and get_timeout_seconds(player) > 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        # if get_timeout_seconds(player) <= 0:
        if timeout_happened:
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")


class PairHiringPC(Page):
    form_model = 'player'
    form_fields = ['worker1_id', 'worker1_gender', 'worker1_race', 'worker1_agegroup',
                   'worker2_id', 'worker2_gender', 'worker2_race', 'worker2_agegroup',]
    # get_timeout_seconds = get_timeout_seconds
    timeout_seconds = C.time_treatment_page
    timer_text = C.TIMER_TEXT

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        worker1_id = participant.decision_pair["worker_id"]
        worker1_gender = participant.decision_pair["gender"]
        worker1_race = participant.decision_pair['race']
        worker1_agegroup = participant.decision_pair['agegroup']
        worker2_id = participant.decision_pair['opponent_id']
        worker2_gender = participant.decision_pair['gender_opp']
        worker2_race = participant.decision_pair['race_opp']
        worker2_agegroup = participant.decision_pair['agegroup_opp']
        # generation of PC decisions:
        """
        p_hired = 0.5
        draws = np.random.poisson(p_hired, size=10)
        num_hirings = sum(draws)
        num_nothired = 10 - num_hirings
        num_hirings_pc = num_hirings * 10
        num_nothired_pc = num_nothired * 10
        if num_hirings_pc > 5:
            participant.bonus_pre_hiring = C.pre_hiring_bonus
        elif num_hirings_pc < 5:
            participant.bonus_pre_hiring = cu(0)
        else:
            participant.bonus_pre_hiring = np.random.choice([cu(0), C.pre_hiring_bonus])
        print ("bonus pre hiring", participant.bonus_pre_hiring)
        """
        treatment = participant.decision_pair['treatment']
        bonus_pre_hiring = participant.bonus_pre_hiring
        num_hirings = participant.num_hirings
        num_nothired = participant.num_nothired
        num_hirings_pc = participant.num_hirings_pc
        num_nothired_pc = participant.num_nothired_pc
        return {'worker1_id': worker1_id,
                'worker1_gender': worker1_gender,
                'worker1_race': worker1_race,
                'worker1_agegroup': worker1_agegroup,
                'worker2_id': worker2_id,
                'worker2_gender': worker2_gender,
                'worker2_race': worker2_race,
                'worker2_agegroup': worker2_agegroup,
                'treatment': treatment,
                'num_hirings': num_hirings,
                'num_nothired': num_nothired,
                'num_hirings_pc': num_hirings_pc,
                'num_nothired_pc': num_nothired_pc,
                'bonus_pre_hiring': bonus_pre_hiring,
                }

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.decision_pair['treatment'] == 4 # and get_timeout_seconds(player) > 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        # if get_timeout_seconds(player) <= 0:
        if timeout_happened:
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")


class PairHiringNoInfo(Page):
    form_model = 'player'
    form_fields = ['worker1_id', 'worker1_gender', 'worker1_race', 'worker1_agegroup',
                   'worker2_id', 'worker2_gender', 'worker2_race', 'worker2_agegroup',]
    # get_timeout_seconds = get_timeout_seconds
    timeout_seconds = C.time_treatment_page
    timer_text = C.TIMER_TEXT

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        worker1_id = participant.decision_pair["worker_id"]
        worker1_gender = participant.decision_pair["gender"]
        worker1_race = participant.decision_pair['race']
        worker1_agegroup = participant.decision_pair['agegroup']
        worker2_id = participant.decision_pair['opponent_id']
        worker2_gender = participant.decision_pair['gender_opp']
        worker2_race = participant.decision_pair['race_opp']
        worker2_agegroup = participant.decision_pair['agegroup_opp']
        hiring_decision_pro = player.participant.decision_pair['decisions_pro']
        hiring_decision_pro_pc = hiring_decision_pro*10
        hiring_decision_con = player.participant.decision_pair['decisions_con']
        hiring_decision_con_pc = hiring_decision_con*10
        treatment = participant.decision_pair['treatment']
        bonus_pre_hiring = participant.bonus_pre_hiring
        return {'worker1_id': worker1_id,
                'worker1_gender': worker1_gender,
                'worker1_race': worker1_race,
                'worker1_agegroup': worker1_agegroup,
                'worker2_id': worker2_id,
                'worker2_gender': worker2_gender,
                'worker2_race': worker2_race,
                'worker2_agegroup': worker2_agegroup,
                'hiring_decision_pro': hiring_decision_pro,
                'hiring_decision_con': hiring_decision_con,
                'hiring_decision_pro_pc': hiring_decision_pro_pc,
                'hiring_decision_con_pc': hiring_decision_con_pc,
                'treatment': treatment,
                'bonus_pre_hiring': bonus_pre_hiring,
                }

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.decision_pair['treatment'] == 3 # and get_timeout_seconds(player) > 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        # if get_timeout_seconds(player) <= 0:
        if timeout_happened:
            if player.participant.label in session.used_labels:
                session.used_labels.remove(player.participant.label)
                session.free_labels.append(player.participant.label)
                print("updated used list", session.used_labels)
                print("updated free labels", session.free_labels)
            else:
                print("label not in used-labels list")


page_sequence = [InstructionsDecisions, PairHiringDiscr, PairHiringNoDiscr, PairHiringPC, PairHiringNoInfo]
