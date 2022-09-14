import enum
from opcode import stack_effect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, asc
from sqlalchemy.orm import sessionmaker 
from datetime import datetime, timedelta

engine = create_engine('sqlite:///tareas_principales.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Tabla(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    tarea = Column(String, default='Tomar agüita')
    fecha_limite = Column(Date, default=datetime.today())

    def __repr__(self) -> str:
        return self.tarea

Base.metadata.create_all(engine)
hoy = datetime.today().date()

class Tareas:
    def __init__(self):
        self.filas = session.query(Tabla).all()
        self.filas_hoy = session.query(Tabla).filter(Tabla.fecha_limite == hoy).all()
        self.opcion_usuario = input(
'''
Menú de tareas:
1) Tareas para hoy
2) Tareas de la semana
3) Todas las tareas
4) Tareas olvidadas
5) Agregar Tarea
6) Borrar tarea
0) Salir
''')
    # 1) Tareas para hoy   
    def opcion_1(self):
        if self.opcion_usuario == '1':
            print(f'\n{hoy}')
            if len(self.filas_hoy) > 0:
                for count, item in enumerate(self.filas_hoy):
                    print(f'{count + 1}. {item}\n')
            else:
                print('No hay tareas para hoy\n')

    # 2) Tareas para la semana (7 días)  
    def opcion_2(self):
        if self.opcion_usuario == '2':
            print(f'\n{hoy}')
            if len(self.filas_hoy) > 0:
                for count, item in enumerate(self.filas):
                    print(f'{count + 1}. {item}\n')
            else:
                print('No hay tareas para hoy\n')

            def semana(n): 
                d = hoy + timedelta(n)
                print(f'{d}:')
                tareas = []
                for j in self.filas:
                    if j.fecha_limite == d:
                        tareas.append(j)
                if len(tareas) > 0:
                    for c, i in enumerate(tareas):
                        print(f'{c + 1}. {i}\n')
                else:
                    print('Nada para hoy\n')

            semana(1) # Mañana
            semana(2) # Pasado mañana
            semana(3) # Día 4
            semana(4) # Día 5
            semana(5) # Día 6
            semana(6) # Día 7

    # 3) Todas las tareas  
    def opcion_3(self):
        if self.opcion_usuario == '3':
            print('\n Todas las tareas:')
            u = session.query(Tabla).order_by(asc(Tabla.fecha_limite)).all()
            if len(u) > 0:
                for count, item in enumerate(u):
                    print(f'{count + 1}. {item}. {item.fecha_limite}')
            
            else:
                print('No hay tareas\n')

    # 4) Tareas olvidadas
    def opcion_4(self):
        if self.opcion_usuario == '4':
            print('\n Treas olvidadas:')
            u = session.query(Tabla).order_by(asc(Tabla.fecha_limite)).all()
            m = []
            for item in u:
                if item.fecha_limite < hoy:
                    m.append(item)
            if len(m) > 0:
                for count, item in enumerate(m):
                    print(f'{count + 1}. {item}. {item.fecha_limite}')
                print()
            else:
                print('Ninguna tarea olvidada\n')

    # 5) Agregar tarea
    def opcion_5(self):
        if self.opcion_usuario == '5':
            print('\nCuál es la tarea?')
            tarea_input = input()
            print('\nIngresa la fecha límite en el siguiente formato (AAAA-MM-DD)')
            limite_input = input()
            x = limite_input.split('-')
            fecha_tarea = datetime(int(x[0]), int(x[1]), int(x[2])).date()
            nueva_tarea = Tabla(tarea=tarea_input, fecha_limite=fecha_tarea)
            session.add(nueva_tarea)
            session.commit()
            print('\n¡La tarea ha sido agregada!\n')

    # 6) Borrar tarea
    def opcion_6(self):
        if self.opcion_usuario == '6':
            u = session.query(Tabla).order_by(asc(Tabla.fecha_limite)).all()
            if len(u) > 0:
                print('\nElige el numero de la tarea que quieres borrar: ')
                for count, item in enumerate(u):
                    print(f'{count + 1}. {item}. {item.fecha_limite}')
                borrar = input()
                for count, item in enumerate(u):
                    if int(borrar) == count + 1:
                        session.delete(item)
                        session.commit()
                        print(f'\n¡La tarea ha sido borrada con éxito\n')
            else:
                print('\nNo hay tareas para borrar\n')

    # 0) Salir del programa
    def opcion_0(self):
        if self.opcion_usuario == '0':
            print('\n¡Hasta pronto!')
            exit()


while True:               
    tareas = Tareas()
    tareas.opcion_1()
    tareas.opcion_2()
    tareas.opcion_3()
    tareas.opcion_4()
    tareas.opcion_5()
    tareas.opcion_6()
    tareas.opcion_0()