def setup(title, details=None):
    box_width = 100
    title = f'► {title} ◄'.center(box_width - 2)  # Ajuste manual do espaçamento
    
    print('╔' + '═' * (box_width - 2) + '╗')
    print(f'║{title}║')
    
    if details:
        for detail in details:
            print(f'║ {detail:<{box_width-4}} ║')  # Ajuste para exibir detalhes
    
    print('╚' + '═' * (box_width - 2) + '╝')