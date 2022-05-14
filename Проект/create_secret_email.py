def cr_sec_email(email):
    email_com = email.split('.')[1]
    email_add = email.split('@')[1].split('.')[0]
    email_add = len(email_add) * '*'
    email_name = email.split('@')[0]
    email_name = email_name[0] + (len(email_name) - 2) * '*' + email_name[-1]
    sec_email = email_name + '@' + email_add + '.' + email_com
    return sec_email