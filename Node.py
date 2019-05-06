class Node:
    f_x = 0
    f_y = 0
    f_z = 0
    m_x = 0
    m_y = 0
    m_z = 0

    d_x = 0
    d_y = 0
    d_z = 0
    dm_x = 0
    dm_y = 0
    dm_z = 0

    td_x = 0
    td_y = 0
    td_z = 0
    tdm_x = 0
    tdm_y = 0
    tdm_z = 0
    
    t_x = None  # t for translations
    t_y = None
    t_z = None
    r_x = None  # r for rotations
    r_y = None
    r_z = None

    def __init__(self, id, p_x, p_y, p_z):
        self.id = id
        self.p_x = p_x  # p for co-ordinate
        self.p_y = p_y
        self.p_z = p_z

        return None