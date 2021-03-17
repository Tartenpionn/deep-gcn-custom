

def extract_vertices(line_list):
    pts = []
    colors = []
    for line in line_list:
        lsp=line.strip('\n').split(' ')
        if lsp[0]=='v':
            pts.append([lsp[1],lsp[2],lsp[3]])
            colors.append([lsp[4],lsp[5],lsp[6]])
    return pts,colors


def read_obj(filename):
    lines = []
    with open(filename,'r') as f:
        for line in f:
            lines.append(line)
    return extract_vertices(lines)
