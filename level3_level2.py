
print('\nbegain to calculate average of lists')
list_a = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
list_b = [3, 5, 1, 2]
list_c = [3]

avg_a = sum(list_a) / len(list_a)
avg_b = sum(list_b) / len(list_b)
avg_c = sum(list_c) / len(list_c)
print('average of list_a:', avg_a)
print('average of list_b:', avg_b)
print('average of list_c:', avg_c)

total_average = (avg_a + avg_b + avg_c) / 3
print('total average:', total_average)



list_total = list_a + list_b + list_c
print('total list:', list_total)
print('total average of all lists:', sum(list_total) / len(list_total))
