@app.route("/get_data", methods=['POST', 'GET'])
def data():
    received_data = request.get_json(force=True)
    a = received_data["a"]
    b = received_data["b"]
    print(a, b)
    df = pd.read_csv("static/js/EQWT.csv")
    column = list(df.columns)
    new_columns = []
    if b['f0'] == True:
        j = 0
        for k in range(0, len(b) - 1):
            new_columns.append(column[j])
        j = j + 1
    else:
        if b['f1'] == True:
            new_columns.append(column[0])
        if b['f2'] == True:
            new_columns.append(column[1])
        if b['f3'] == True:
            new_columns.append(column[2])
        if b['f4'] == True:
            new_columns.append(column[3])
        if b['f5'] == True:
            new_columns.append(column[4])
        if b['f6'] == True:
            new_columns.append(column[5])


    df_alerts = df[df['has_alerted'] == 1]
    df_nonalerts = df[df['has_alerted'] == 0]
    df_escalations = df[df['has_escalated'] == 1]
    result = {}
    if a['all'] == True:
        for column in new_columns:
            result[column]['non-alerts'] = (list(df_nonalerts[column]))
            result[column]['alerts'] = (list(df_alerts[column]))
            result[column]['escalations'] = (list(df_escalations[column]))

    else:
        for column in new_columns:
            result[column] = {}
            for keys in a:
                if a[keys] == True:
                    if keys == 'non-alert':
                        result[column]['non-alerts'] = (list(df_nonalerts[column]))
                    if keys == 'alert':
                        result[column]['alerts'] = (list(df_alerts[column]))
                    if keys == 'escalations':
                        result[column]['escalations'] = (list(df_escalations[column]))
                    
                else:
                    if keys == 'All':
                        continue
                    else:
                        if keys == 'non-alert':
                            result[column]['non-alerts'] = []
                        if keys == 'alert':
                            result[column]['alerts'] = []
                        if keys == 'escalations':
                            result[column]['escalations'] = []


    return jsonify(result)
