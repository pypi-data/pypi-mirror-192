from datetime import datetime, timedelta
import ipdb

class ConfigDate:
    def dateDeltaFuture(delta, formato):
        initialTime = datetime.now()
        deltaTime   = initialTime + timedelta(days = delta)

        formatDate  = deltaTime.strftime(formato)

        return formatDate
    
    def dateDeltaPast(delta, formato):
        initialTime = datetime.now()
        deltaTime   = initialTime - timedelta(days = delta)

        formatDate  = deltaTime.strftime(formato)

        return formatDate
    
    def generateTextStatistics(delta):
        initialTime = datetime.now()
        deltaTime   = initialTime - timedelta(days = delta)

        month = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

        formatDate  = deltaTime.strftime('%m%Y')
        monthDate = month[int(deltaTime.strftime('%m'))]

        finalText = formatDate + ' - ' + monthDate
        
        return finalText
    
    def generateTextWiki(delta):
        initialTime = datetime.now()
        deltaTime   = initialTime - timedelta(days = delta)

        month = {1: '_jan', 2: '_fev', 3: '_mar', 4: '_abr', 5: '_mai', 6: '_jun', 7: '_jul', 8: '_ago', 9: '_set', 10: '_out', 11: '_nov', 12: '_dez'}

        formatDate  = deltaTime.strftime('%m%Y')
        monthDate = month[int(deltaTime.strftime('%m'))]
        
        return monthDate