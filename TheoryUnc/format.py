with open(r'../VBFAnalysis/data/PMGxsecDB_mc16_dup.txt', 'r') as f:
    for line in f:
        data = line.split()    # Splits on whitespace
        if len(data) <2:
            print(f'{data[0]:<15}')
        elif len(data) <9:
            print(f'{data[0]:<15}{data[1]:<60}{data[2]:<15}{data[3]:<20}{data[4]:<15}{data[5]:<15}{data[6]:<15}{data[7]:<15}')
        elif len(data) >8:
            print(f'{data[0]:<15}{data[1]:<60}{data[2]:<15}{data[3]:<20}{data[4]:<15}{data[5]:<15}{data[6]:<15}{data[7]:<15}{data[8]:<15}')
