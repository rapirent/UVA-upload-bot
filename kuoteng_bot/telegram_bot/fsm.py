from transitions.extensions import GraphMachine

machine = GraphMachine(
    states=[
        '()not_have_used_start_to_set',
        '(-1)uva_unenroll_user',
        '(0)uva_enrolled_user',
        '(>-1)upload_file_to_uva',
        '(*)use_start_to_set',
        '(1)want_to_set_uva_id',
        '(2)want_to_set_uva_passwd',
        '(!=1||!=2)echo',
        'set_uva_id',
        'set_uva_passwd',
        'show_fsm',
        'show_uva_info',
        'show_help_info',
        'search_weather_info'
    ],
    transitions=[

        {
            'trigger': 'go_back',
            'source': 'search_weather_info',
            'dest': '()not_have_used_start_to_set',
            'conditions': 'not found in database'
        },
         {
            'trigger': 'go_back',
            'source': 'search_weather_info',
            'dest': '(-1)uva_unenrolled_user',
            'conditions': 'database states is in -1'
        },
         {
            'trigger': 'go_back',
            'source': 'search_weather_info',
            'dest': '(0)uva_enrolled_user',
            'conditions': 'database states is in 0'
        },
         {
            'trigger': 'go_back',
            'source': 'search_weather_info',
            'dest': '(1)want_to_set_uva_id',
            'conditions': 'database states is in 1'
        },
         {
            'trigger': 'go_back',
            'source': 'search_weather_info',
            'dest': '(2)want_to_set_uva_passwd',
            'conditions': 'database states is in 2'
        },
       {
            'trigger': 'send_location',
            'source': [
                '()not_have_used_start_to_set',
                '(-1)uva_unenroll_user',
                '(0)uva_enrolled_user',
                '(1)want_to_set_uva_id',
                '(2)want_to_set_uva_passwd',
            ],
            'dest': 'search_weather_info',

        },
        {
            'trigger': 'go_back',
            'source': 'show_help_info',
            'dest': '()not_have_used_start_to_set',
            'conditions': 'not found in database'
        },
         {
            'trigger': 'go_back',
            'source': 'show_help_info',
            'dest': '(-1)uva_unenrolled_user',
            'conditions': 'database states is in -1'
        },
         {
            'trigger': 'go_back',
            'source': 'show_help_info',
            'dest': '(0)uva_enrolled_user',
            'conditions': 'database states is in 0'
        },
         {
            'trigger': 'go_back',
            'source': 'show_help_info',
            'dest': '(1)want_to_set_uva_id',
            'conditions': 'database states is in 1'
        },
         {
            'trigger': 'go_back',
            'source': 'show_help_info',
            'dest': '(2)want_to_set_uva_passwd',
            'conditions': 'database states is in 2'
        }, 
        {
            'trigger': 'go_back',
            'source': 'send_back_sticker',
            'dest': '()not_have_used_start_to_set',
            'conditions': 'not found in database'
        },
         {
            'trigger': 'go_back',
            'source': 'send_back_sticker',
            'dest': '(-1)uva_unenrolled_user',
            'conditions': 'database states is in -1'
        },
         {
            'trigger': 'go_back',
            'source': 'send_back_sticker',
            'dest': '(0)uva_enrolled_user',
            'conditions': 'database states is in 0'
        },
         {
            'trigger': 'go_back',
            'source': 'send_back_sticker',
            'dest': '(1)want_to_set_uva_id',
            'conditions': 'database states is in 1'
        },
         {
            'trigger': 'go_back',
            'source': 'send_back_sticker',
            'dest': '(2)want_to_set_uva_passwd',
            'conditions': 'database states is in 2'
        },
       {
            'trigger': 'send_sticker',
            'source': [
                '()not_have_used_start_to_set',
                '(-1)uva_unenroll_user',
                '(0)uva_enrolled_user',
                '(1)want_to_set_uva_id',
                '(2)want_to_set_uva_passwd',
            ],
            'dest': 'send_back_sticker'

        },
       {
            'trigger': '/help',
            'source': [
                '()not_have_used_start_to_set',
                '(-1)uva_unenroll_user',
                '(0)uva_enrolled_user',
                '(>-1)upload_file_to_uva',
                '(*)use_start_to_set',
                '(1)want_to_set_uva_id',
                '(2)want_to_set_uva_passwd',
                ],
            'dest': 'show_help_info',
        },
        {
            'trigger': 'go_back',
            'source': 'show_uva_info',
            'dest': '(0)uva_enrolled_user',
        },
        {
            'trigger': 'go_back',
            'source': 'show_uva_info',
            'dest': '(1)want_to_set_uva_id',
        },
        {
            'trigger': 'go_back',
            'source': 'show_uva_info',
            'dest': '(2)want_to_set_uva_passwd'
        },
       {
            'trigger': '/uva',
            'source': [
                   '(0)uva_enrolled_user',
                    '(1)want_to_set_uva_id',
                    '(2)want_to_set_uva_passwd'
                ],
            'dest': 'show_uva_info',
            'conditions': 'user enroll uva info'
        },
        {
            'trigger': '/uva',
            'source': '()not_have_used_start_to_set',
            'dest': '()not_have_used_start_to_set',
            'conditions': 'user not enroll uva info',
        },
        {
            'trigger': '/uva',
            'source': '(-1)uva_unenroll_user', 
            'dest': '(-1)uva_unenroll_user', 
            'conditions': 'user not enroll uva info',
        },
        {
            'trigger': '/uva',
            'source': '(1)want_to_set_uva_id',
            'dest': '(1)want_to_set_uva_id',
            'conditions': 'user not enroll uva info',
        },
         {
            'trigger': '/uva',
            'source': '(2)want_to_set_uva_passwd',
            'dest': '(2)want_to_set_uva_passwd',
            'conditions': 'user not enroll uva info',
        },
       {
            'trigger': '/start',
            'source': [
                    '()not_have_used_start_to_set',
                    '(-1)uva_unenroll_user',
                    '(0)uva_enrolled_user',
                    '(1)want_to_set_uva_id',
                    '(2)want_to_set_uva_passwd'
                ],
            'dest': '(*)use_start_to set',
        },
        {
            'trigger': 'go_back',
            'source': '(*)use_start_to_set',
            'dest': '(-1)uva_unenrolled_user',
            'conditions': 'database states is in -1'
        },
        {
            'trigger': 'go_back',
            'source': '(*)use_start_to_set',
            'dest': '(0)uva_enrolled_user',
            'conditions': 'database states is in 0'
        },
        {
            'trigger': 'go_back',
            'source': '(*)use_start_to_set',
            'dest': '(1)want_to_set_uva_id',
            'conditions': 'database states is in 1'
        },
        {
            'trigger': 'go_back',
            'source': '(*)use_start_to_set',
            'dest': '(2)want_to_set_uva_passwd',
            'conditions': 'database states is in 2'
        },
        {
            'trigger': 'send_text',
            'source': [
                    '()not_have_used_start_to_set',
                    '(-1)uva_unenroll_user',
                    '(0)uva_enrolled_user',
                ],
            'dest': '(!=1||!=2)echo',
            'conditions': 'database states not 1 or 2',
        },
        {
            'trigger': 'send_file',
            'source': '()not_have_used_start_to_set',
            'dest': '()not_have_used_start_to_set',
            'conditions': 'not found in database'
        },
        {
            'trigger': 'send_file',
            'source': '(-1)uva_unenrolled_user',
            'dest': '(-1)uva_unenrolled_user',
            'conditions': 'database states is -1'
        },
        {
            'trigger': 'send_file',
            'source': [
                    '(0)uva_enrolled_user',
                    '(1)want_to_set_uva_id',
                    '(2)want_to_set_uva_passwd'
                ],
            'dest': '(>-1)upload_file_to_uva',
            'conditions': 'database states > -1'
        },
        {
            'trigger': 'go_back',
            'source': '(>-1)upload_file_to_uva',
            'dest': '(0)uva_enrolled_user',
            'conditions': 'database states is in 0'
        },
        {
            'trigger': 'go_back',
            'source': '(>-1)upload_file_to_uva',
            'dest': '(1)want_to_set_uva_id',
            'conditions': 'database states is in 1'
        },
        {
            'trigger': 'go_back',
            'source':  '(>-1)upload_file_to_uva',
            'dest': '(2)want_to_set_uva_passwd',
            'conditions': 'database states is in 2'
        },
        {
            'trigger': 'choose_set_id',
            'source': [
                '(*)use_start_to_set',
                '(-1)uva_unenroll_user',
                '(0)uva_enrolled_user'
                ],
            'dest': '(1)want_to_set_uva_id'
        },
        {
            'trigger': 'choose_set_passwd',
            'source': [
                '(*)use_start_to_set',
                '(-1)uva_unenroll_user',
                '(0)uva_enrolled_user'
            ],
            'dest': '(2)want_to_set_uva_passwd'
        },
        {
            'trigger': 'send_text',
            'source': '(1)want_to_set_uva_id',
            'dest': 'set_uva_id',
            'conditions': 'in states 1'
        },
        {
            'trigger': 'send_text',
            'source': '(2)want_to_set_uva_passwd',
            'dest': 'set_uva_passwd',
            'conditions': 'in states 2'
        },
        {
            'trigger': 'go back',
            'source': [
                    'set_uva_id',
                    'set_uva_passwd'
                ],
            'dest': '(0)uva_enrolled_user'
        },
        {
            'trigger': '/fsm',
            'source': [
                    '()not_have_used_start_to_set',
                    '(-1)uva_unenroll_user',
                    '(0)uva_enrolled_user',
                    '(1)want_to_set_uva_id',
                    '(2)want_to_set_uva_passwd' 
                ],
            'dest': 'show_fsm'
        },
        {
            'trigger': 'go_back',
            'source': 'show_fsm',
            'dest': '()not_have_used_start_to_set',
            'conditions': 'not found in database'
        },
        {
            'trigger': 'go_back',
            'source': 'show_fsm',
            'dest': '(-1)uva_unenrolled_user',
            'conditions': 'database states is -1'
        },
        {
            'trigger': 'go_back',
            'source': 'show_fsm',
            'dest': '(0)uva_enrolled_user',
            'conditions': 'database states is 0'
        },
        {
            'trigger': 'go_back',
            'source': 'show_fsm',
            'dest': '(1)want_to_set_uva_id',
            'conditions': 'database states is 1'
        },
        {
            'trigger': 'go_back',
            'source': 'show_fsm',
            'dest': '(2)want_to_set_uva_passwd',
            'conditions': 'database states is 2'
        }        
    ],
    initial='()not_have_used_start_to_set',
    auto_transitions=False,
    show_conditions=True,
)


##useless
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        return text.lower() == 'go to state1'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def on_enter_state1(self, update):
        update.message.reply_text("I'm entering state1")
        self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("I'm entering state2")
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

#if __name__ == "__main__":
    #main()
