import numpy as np


class Node:
    f_x = 0.0
    f_y = 0.0
    f_z = 0.0
    m_x = 0.0
    m_y = 0.0
    m_z = 0.0

    d_x = 0.0
    d_y = 0.0
    d_z = 0.0
    dm_x = 0.0
    dm_y = 0.0
    dm_z = 0.0

    td_x = 0
    td_y = 0
    td_z = 0
    tdm_x = 0
    tdm_y = 0
    tdm_z = 0

    t_x = False  # t for translations
    t_y = False
    t_z = False
    r_x = False  # r for rotations
    r_y = False
    r_z = False

    def __init__(self, id, p_x, p_y, p_z):
        self.id = id
        self.p_x = p_x  # p for co-ordinate
        self.p_y = p_y
        self.p_z = p_z

        return None

    def get_dof(self):
        dofs = np.array([self.f_x, self.f_y, self.f_z, self.m_x, self.m_y, self.m_z], dtype=np.float_)
        restrains = [self.t_x, self.t_y, self.t_z, self.r_x, self.r_y, self.r_z]
        for i in range(6):
            if restrains[i] == True:
                dofs[i] = None

        return dofs

