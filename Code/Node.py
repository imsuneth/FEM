import numpy as np
from DOF import DOF


class Node:
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

    def __init__(self, id, p_x, p_y, p_z, f_x, f_y, f_z, m_x, m_y, m_z, t_x, t_y, t_z, r_x, r_y, r_z):
        self.id = id
        self.p_x = p_x  # p for co-ordinate
        self.p_y = p_y
        self.p_z = p_z
        self.f_x = f_x
        self.f_y = f_y
        self.f_z = f_z
        self.m_x = m_x
        self.m_y = m_y
        self.m_z = m_z
        self.t_x = t_x
        self.t_y = t_y
        self.t_z = t_z
        self.r_x = r_x
        self.r_y = r_y
        self.r_z = r_z

        return None

    def get_dof(self):
        dofs = np.array(
            [self.f_x.value, self.f_y.value, self.m_z.value],
            dtype=np.float_)
        restrains = [self.t_x, self.t_y, self.t_z, self.r_z]
        for i in range(3):
            if restrains[i]:
                dofs[i] = None

        return dofs
