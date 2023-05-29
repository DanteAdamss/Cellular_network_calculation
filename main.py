import math
import scipy.integrate as spi
import numpy as np
# test data
F = "880-915"
F_min = 880;F_max = 915 # виділені частоти
F_k = 0.1 # шрина каналу МГц
n_a = 8 # число абонентів на один канал
Na = 25000 # число абонентів до обслуговування
N_activ = 0.025 # активність одного абонента в Ерглангах
P_block = 0.1 # імовірність блокування виклику
P_safty = 9 # захистне відношення, дБ
P_t = 10 # допустимий відсоток часу з погіршеними характеристиками
S = 10 # проща покриття км^2
Gain_ms = -120 # Чутливість приймача MC, дБм
G_bs = 6 # підсилення антени БС, дБ
H_bs = 30 #висота підвісу
# const
alfa = 10 # діапазон випадкових флуктуацій
h_ms = 1.5 # середня висота розміщення МС

print(" ПРОГРАМА: РОЗРАХУНОК БАЗОВИХ ПАРАМЕТРІВ БС МОБІЛЬНОГО ЗВ'ЯЗКУ")
input(" =============================================================")

print(" підсказка: якщо в подальшому розділі ви не введете всі запитувані змінні то програма ")
input(" перейде в тестовий режим і розрахує мережу з такими параметрами: ")
print()
print("    Смуга частот у МГц що доступна (min-max):",F)
print("    Ширина одного частотного каналу(МГц):",F_k)
print("    Тип мережі (LTE or VMT): LTE")
print("    Число абонентів що треба забезпечити зв'язком",Na)
print("    Активність одного абонента в годнину найбільшого навантаження(в Ерл):",N_activ)
print("    Допустима імовірність блокування виклику:",P_block)
print("    Необхідне захистне відношення для приймачів:",P_safty)
print("    Відсоток часу проятгом якого допускається погіршення Захисного відношення:",P_t)
print("    Плоша необхідна для покриву(в км^2):",S)
print("    Чутливість в дБ * Вт приймача МС:",Gain_ms)
print("    Коефіціент підсилення антени БС(в дБ):",G_bs)
print("    Висота підвісу антени БС(в м):",H_bs)
input()
print(" підсказка: якщо хочете відразу зробити тестовий розрахунок то в першому ж полі натисніть 'Enter' ")
input(" -------------------------------------------------------------")
# Змінні та їх введення
try:
    F = str(input(" Смуга частот у МГц що доступна (min-max): "))
    F_min, F_max = map(int, F.split("-"))
    F_k = float(input(" Ширина одного частотного каналу(МГц): "))
    n_a = str(input(" Тип мережі (LTE або VMT або інша кількість користувачів на 1 канал): "))
    if n_a == 'LTE' :
        n_a = int(8)
    elif n_a == 'VMT':
        n_a = int(1)
    else:
        n_a = int(n_a)
    Na = int(input(" Число абонентів що треба забезпечити зв'язком: "))
    N_activ = float(input(" Активність одного абонента в годнину найбільшого навантаження(в Ерл): "))
    P_block = float(input(" Допустима імовірність блокування виклику: "))
    P_safty = float(input(" Необхідне захистне відношення для приймачів: "))
    P_t = int(input(" Відсоток часу проятгом якого допускається погіршення Захисного відношення: "))
    S = float(input(" Плоша необхідна для покриву(в км^2): "))
    Gain_ms = float(input(" Чутливість в дБ * Вт приймача МС: "))
    G_bs = float(input(" Коефіціент підсилення антени БС(в дБ): "))
    H_bs = float(input(" Висота підвісу антени БС(в м): "))
except:
    pass
#print(F_min, F_max, F_k, n_a, Na, N_activ, P_block, P_safty, P_t, S, Gain_ms, G_bs ) #всі введені змінні
#розрахунок числа каналів
n_k = (F_max-F_min)/F_k
#розрахунок розмірності кластера
def kluster_size(antena_sector_count, propouse_size):
    K = propouse_size
    M = antena_sector_count
    q = math.sqrt(3 * K)
    gama = float(f"{0.1 * math.log(10):.2f}")
    if M == 1:
        beta1 = beta2 = beta3 = beta4 = beta5 = beta6 = 0
        beta1 = (q - 1) ** (-4)
        beta2 = beta1
        beta3 = q ** (-4)
        beta4 = beta3
        beta5 = (q + 1) ** (-4)
        beta6 = beta5
        beta_sum = beta1 + beta2 + beta3 + beta4 + beta5 + beta6
        a_e_2 = (1 / (gama ** 2)) * math.log(1 + (math.exp((gama ** 2) * (alfa ** 2)) - 1) * (((beta1 ** 2) + (beta2 ** 2) + (beta3 ** 2) + (beta4 ** 2) + (beta5 ** 2) + (beta6 ** 2)) / (beta_sum ** 2)))
    elif M == 3:
        beta1 = beta2 = beta3 = beta4 = beta5 = beta6 = 0
        beta1 = (q + 1) ** (-4)
        beta2 = q ** (-4)
        beta_sum = beta1 + beta2
        a_e_2 = (1 / (gama ** 2)) * math.log(1 + (math.exp((gama ** 2) * (alfa ** 2)) - 1) * (((beta1 ** 2) + (beta2 ** 2)) / (beta_sum ** 2)))
    elif M == 6:
        beta1 = beta2 = beta3 = beta4 = beta5 = beta6 = 0
        beta_sum = (q + 1) ** (-4)
        a_e_2 = (1 / (gama ** 2)) * math.log(1 + (math.exp((gama ** 2) * (alfa ** 2)) - 1))
    beta_e = beta_sum*math.exp((gama**2/2)*(alfa**2 - a_e_2))
    a_p_2 = alfa**2 +a_e_2
    a_p = math.sqrt(a_p_2)
    x1 = (10*math.log(1/beta_e,10)-P_safty)/(a_p)
    P_t_now, _ = spi.quad(lambda x: (1/np.sqrt(2*np.pi)) * np.exp(-x**2/2), x1, np.inf)
    Pn = P_t_now * 100
    #return  q,  beta_sum, a_e_2, beta1, beta2 , beta3, beta4, beta5, beta6 , beta_sum, beta_e , a_p, x1, P_t_now, Pn #вивід всіх обрахунків
    #print(beta_sum,q,a_e_2,beta_e,a_p,a_p_2,x1)#test
    return Pn
Pn_list = []
    #розрахунок % часу нищого за захисний % при всенаправленій антені
N = 1; M = 1
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
N = 3; M = 1
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
N = 6; M = 1
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
    #розрахунок % часу нищого за захисний % при анетені 120гард.
N = 1; M = 3
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
N = 3; M = 3
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
N = 6; M = 3
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
    #розрахунок % часу нищого за захисний % при анетені 60гард.
N = 1; M = 6
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
N = 3; M = 6
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
N = 6; M = 6
Temp_list = [kluster_size(M,N), M, N]
Pn_list.append(Temp_list)
closest_sublist = None
closest_difference = float('inf')
for sublist in Pn_list:
    difference = abs(sublist[0] - P_t)
    if difference < closest_difference:
        closest_difference = difference
        closest_sublist = sublist
Pn, M, N = closest_sublist
#число частотних каналів в одному секторі стільника
n_s = int(n_k/(M*N))
while n_s == 0 :
    F_k = float(input(" Замала кількість каналів, спробуйте зменшити ширину одного каналу(МГц): "))
    n_k = (F_max - F_min) / F_k
    n_s = int(n_k / (M * N))
#припустиме телефонне навантаження
n0 = n_a * n_s
while True:
    try:
        if P_block <= 2 / (math.pi * n0):
            A = n0 * (1 - math.sqrt(1 - (P_block * math.sqrt((math.pi * n0) / 2)) ** (1 / n0)))
        else:
            A = n0 + math.sqrt(math.pi / 2 + 2 * n0 * math.log(P_block * math.sqrt((math.pi * n0) / 2))) - math.sqrt(math.pi / 2)
        break
    except ValueError:
        print(" Під коренем опинилося відємне число. Спробуйте замінити значення імовірності блокування виклику")
        P_block = float(input(" Нове значення імовірності блокування виклику: "))
#число абонетів на одну БС
N_bs = math.floor(A/N_activ)
#число БС у мережі
K = math.ceil(Na/N_bs)
#радіус одної БС
R0 = float(f"{math.sqrt(S/(math.pi*K)):.2f}")
#потужність передавача БС
rounded_F_min = math.ceil(F_min / 100) * 100
rounded_F_max = math.floor(F_max / 100) * 100
if abs(F_min - rounded_F_min) < abs(F_max - rounded_F_max):
    F_round = rounded_F_min
else:
    F_round = rounded_F_max
P_bs = float(f"{-(G_bs - 70 - 26.16 * math.log10(F_round) + 13.82 * math.log10(H_bs) - (45 - 6.55 * math.log10(H_bs)) * math.log10(R0)) + Gain_ms:.2f}")
#print(n_k, N,M, Pn,"ns=",n_s,n0,A,N_bs,K,R0, F_round, P_bs) #test
#вивід параметрів
print(" ================================================================")
print(" Отже, оптимальні базові параметри БС з вказаними данними такі: ")
print(" Оптимальна розмірність кластера:",N)
print(" Число сектоів в одному стільнику:",M)
print(" Кількість БС що необхідно встановити:",K)
print(" Радіус одної БС:",R0," км^2")
print(" Потужність передавача БС:",P_bs,"дБ*Вт")

