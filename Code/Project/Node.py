class Node:
    id = None
    p_x = None
    p_y = None
    p_z = None
    f_x = None
    f_y = None
    f_z = None
    m_x = None
    m_y = None
    m_z = None
    d_x = None
    d_y = None
    d_z = None
    c_x = None
    c_y = None
    c_z = None
    c_mx = None
    c_my = None
    c_mz = None

    def __init__(self, id, p_x, p_y, p_z, f_x, f_y, f_z, m_x, m_y, m_z, d_x, d_y, d_z, c_x, c_y, c_z, c_mx, c_my, c_mz):
        self.id = id
        self.p_x = p_x
        self.p_y = p_y
        self.p_z = p_z
        self.f_x = f_x
        self.f_y = f_y
        self.f_z = f_z
        self.d_x = d_x
        self.d_y = d_y
        self.d_z = d_z

        return None
