# Python 2.7.5
# Wyatt Wolf


class Parser:

    def __init__(self, t_list):
        self.token_list = t_list
        self.lookahead = 0

    def print_error(self):
        print('Error on Line: ' + str(self.token_list[self.lookahead - 1].line_num) + ' char: ' +
              str(self.token_list[self.lookahead - 1].character_num))

    def parse_token_list(self):
        self.program()

    # <vars> program <block>
    def program(self):
        # <vars>
        self.vars()

        # program
        if self.token_list[self.lookahead].tokenID == 'program_tk':
            self.lookahead += 1
            # <block>
            self.block()
        else:
            self.print_error(self.lookahead)
            print('Invalid declaration statement or missing \'Program\' keyword after variable declaration(s)')
            exit(1)

    # begin <vars> <stats> end
    def block(self):
        # begin
        if self.token_list[self.lookahead].tokenID == 'begin_tk':
            self.lookahead += 1
            # <vars>
            self.vars()
            # <stats>
            self.stats()
            # end
            if self.token_list[self.lookahead].tokenID == 'end_tk':
                # valid syntax
                return
            else:
                self.print_error()
                print('Block statement expected to end with keyword: end')
                exit(1)
        else:
            self.print_error()
            print('Block statement expected to start with keyword: begin')
            exit(1)

    def expr(self):
        return

        # <stat> <mStat>
    def check_semicolin(self):
        if self.token_list[self.lookahead].tokenID == 'SMICLN_tk':
            self.lookahead += 1
            return
        else:
            print('Error Semicolin expected.')
            self.print_error()
            exit(1)

    def stats(self):
        self.stat()
        self.mstat()
        return

    def stat(self):
        ll_id = self.token_list[self.lookahead].tokenID
        if ll_id == 'input_tk': # <in>
            self.input_tk()
            self.check_semicolin()
        elif ll_id == 'output_tk': # <out>
            self.output_tk()
            self.check_semicolin()
        elif ll_id == 'begin_tk': # <block>
            self.block()
        elif ll_id == 'if_tk':
            self.if_tk()
            self.check_semicolin()
        elif ll_id == 'while_tk':
            self.while_tk()
            self.check_semicolin()
        elif ll_id == 'assign_tk':
            self.assign_tk()
            self.check_semicolin()
        elif ll_id == 'warp_tk':
            self.warp_tk()
            self.check_semicolin()
        elif ll_id == 'label_tk':
            self.label_tk()
            self.check_semicolin()
        else:
            print('Error! Statement expected.')
            self.print_error()
            exit(1)
        return

    def mstat(self):
        first_stat = {'input_tk', 'output_tk', 'begin_tk', 'if_tk', 'while_tk',
                      'assign_tk', 'warp_tk', 'label_tk'}
        if first_stat.__contains__(self.token_list[self.lookahead].tokenID):
            self.stat()
            self.mstat()
            return
        else:  # empty
            return

    # <label>
    def label_tk(self):
        if self.token_list[self.lookahead].tokenID == 'label_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                return
            else:
                print('Identifier expected after \'label\' token')
                self.print_error()
                exit(1)
        else:
            exit(1)

    # <goto>
    def warp_tk(self):
        if self.token_list[self.lookahead].tokenID == 'warp_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                return
            else:
                print('Error! Identifier expected')
                self.print_error()
                exit(1)
        else:
            exit(1)

    def assign_tk(self):
        return
    def while_tk(self):
        return

    def if_tk(self):
        return
    #TODO add following
    #<if> -> if [ <expr> <RO> <expr> ] then <stat> |
    #if [ <expr> <RO> <expr> ] then <stat> pick <stat>

    # <out>
    def output_tk(self):
        if self.token_list[self.lookahead].tokenID == 'output_tk':
            self.lookahead += 1
            self.expr()
        else:
            exit(1)

    # <in>
    def input_tk(self):
        if self.token_list[self.lookahead].tokenID == 'input_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                return
            else:
                print('Input keyword should be followed by an identifier.')
        else:
            print('You shouldnt be here! Erron in: input_tk() ')
            exit(1)

    # whole Identifier := Integer ; <vars>
    def vars(self):
        # whole
        if self.token_list[self.lookahead].tokenID == 'whole_tk':
            self.lookahead += 1
            # Identifier
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                # :=
                if self.token_list[self.lookahead].tokenID == 'DTDTEQ_tk':
                    self.lookahead += 1
                    # Integer
                    if self.token_list[self.lookahead].tokenID == 'NUM_tk':
                        self.lookahead += 1
                        # ;
                        if self.token_list[self.lookahead].tokenID == 'SMICLN_tk':
                            self.lookahead += 1
                            # <vars>
                            self.vars()

                        else:
                            self.print_error(self.lookahead)
                            print('Semicolon expected at end of variable declaration')
                            exit(1)

                    else:
                        self.print_error(self.lookahead)
                        print('Number expected after assignment operator in variable declaration statement')
                        exit(1)

                else:
                    self.print_error(self.lookahead)
                    print('\':=\' operator expected after variable name in declaration statement')
                    exit(1)

            else:
                self.print_error(self.lookahead)
                print('Identifier expected after whole keyword.')
                exit(1)
