"""
KPI Performance Management System
----------------------------------
A modular OOP-based system for managing:
- Organizations
- Scorecards
- Objectives
- Measures
- Risk calculation
- Performance visualization (Matplotlib)

Built using clean architecture principles.
"""
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from datetime import datetime

class Organization:
    def __init__(self,id,name,sector):
        self.id = id
        self.name = name
        self.sector = sector
        self.scorecards_list = []
        self.active_cycle = "غير نشطة"
        self.scorecard_counter = 0

    def is_active_cycle(self):
       if self.active_cycle == "غير نشطة":
           return False
       else:
           return True
    def generate_scorecard_id(self):
        self.scorecard_counter +=1
        return self.scorecard_counter
    def add_scorecard(self,name,start_date,end_date):
        new_id = self.generate_scorecard_id()
        scorecard = Scorecard(new_id,name,start_date,end_date)
        self.scorecards_list.append(scorecard)
        return scorecard

class KPI_System:
    def __init__(self):
        self.organization_list =[]
        self.organization_list_counter = 0
    def generate_org_id(self):
        self.organization_list_counter +=1
        return self.organization_list_counter
    def add_organization(self,name, sector):
        new_id = self.generate_org_id()
        org = Organization(new_id,name,sector)
        self.organization_list.append(org)
        return org
    def get_organization(self,org_id):
        for org in self.organization_list:
         if org.id == org_id :
             return org
        return None
    def delete_organization(self,id):
        for org in self.organization_list:
         if org.id == id:
             self.organization_list.remove(org)
             return True
        return False
class Scorecard:
    def __init__(self,id,name,start_date,end_date,):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.objectives_list = []
        self.objective_counter =0
    def generate_objective_id(self):
        self.objective_counter +=1
        return self.objective_counter
    def add_objective(self,name,description,start_date,end_date):
        new_id = self.generate_objective_id()
        objective = Objective(new_id,name,description,start_date,end_date)
        self.objectives_list.append(objective)
        return objective
class Objective:
    def __init__(self,id,name,description,start_date,end_date):
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.measures_list = []
        self.measure_counter =0
    def generate_measure_id(self):
        self.measure_counter +=1
        return self.measure_counter
    def add_measure(self,name,target,unit):
        new_id = self.generate_measure_id()
        measure = Measure(new_id,name,target,unit)
        self.measures_list.append(measure)
        return measure

class Measure:
    def __init__(self,id,name,target,unit):
        self.id = id
        self.name = name
        self.target = target
        self.unit = unit
        self.value_list = []
    def add_value(self,date,value):
        self.value_list.append((date,value))
    def latest_value(self):
        if len(self.value_list) == 0:
            return None
        else:
            return self.value_list[-1][1]
    def calculate_progress(self):
        last_value = self.latest_value()
        if last_value  == None:
            return 0
        else:
         progress = last_value / self.target *100
        return progress
    def calculate_risk(self):
        progress = self.calculate_progress()
        if progress == 0:
            return "High Risk"
        elif progress < 70:
            return "High Risk"
        elif 70 <= progress < 100:
            return "Medium Risk"
        elif progress >= 100:
            return "Low Risk"

    def get_dates(self):
        get_datas = []
        for value in self.value_list :
            get_datas.append(value[0])
        return  get_datas
    def get_values(self):
        get_values = []
        for value in self.value_list:
            get_values.append(value[1])
        return get_values
class PlotService:
    def plot_line(self, measure):
        datas = measure.get_dates()
        values = measure.get_values()
        if not datas:
            print("لا توجد بيانات للرسم")
            return
        reshaped_title = arabic_reshaper.reshape(measure.name)
        bidi_title = get_display(reshaped_title)

        reshaped_x = arabic_reshaper.reshape("التاريخ")
        bidi_x = get_display(reshaped_x)

        reshaped_y = arabic_reshaper.reshape("القيمة")
        bidi_y = get_display(reshaped_y)

        plt.title(bidi_title)
        plt.xlabel(bidi_x)
        plt.ylabel(bidi_y)
        plt.grid(True)
        risks =measure.calculate_risk()
        colors = {
            "High Risk": "red",
            "Medium Risk": "orange",
            "Low Risk": "green"
        }
        color=colors.get(risks, "blue")
        plt.plot(datas, values, linewidth=2, marker='o',color=color)
        plt.grid(True)
        plt.show()

kpi = KPI_System()

org = kpi.add_organization("وزارة الصحة", "قطاع حكومي")

score = org.add_scorecard(
    "الخطة الاستراتيجية 2026",
    "01-01-2026",
    "31-12-2026"
)
obj = score.add_objective("تحسين الأداء", "رفع الكفاءة", "01-01-2026", "31-12-2026")

measure = obj.add_measure("معدل الإنجاز", 100, "%")

measure.add_value(datetime.now(), 60)
measure.add_value(datetime.now(), 75)

plotter = PlotService()
plotter.plot_line(measure)
