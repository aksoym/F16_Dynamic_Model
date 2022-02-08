# F16_Dynamic_Model

## Yapılacaklar:

- Cm-alpha, CL-alpha vb. grafiklerini gösteren fonksiyonlar (monitoring tools) yazılacak. 
- LQR ile SAS kurgusu yazılacak, amaç Cm-alpha, CL vb. gibi değerleri stabil bölgeden çıkartacak manevralara, karşı manevra oluşturacak (elevator, aileron, rudder, thrust)
kontrol girdilerini kontrolcüye verdirmek.
- Son olarak yazılan modellerin/kodun genel olarak (aero_model, propulsion_model gibi) nesne tabanlı hale (class objelerine) dönüştürülmesi. Örneğin Aero_model diye bir class 
oluşturulması ve 'get_aero_forces', 'get_aero_moments' fonksiyonlarının bu class'ın metodu haline getirilmesi.

Referans rapor: [NASA Technical Report 1538](https://core.ac.uk/download/pdf/42866809.pdf)




CL-Alpha grafiği Model vs. Referans

<img src="https://user-images.githubusercontent.com/47147130/125116384-5275e700-e0f5-11eb-94a4-12fcab0b720f.png" height="400"><img src="https://user-images.githubusercontent.com/47147130/125116506-7d603b00-e0f5-11eb-9393-6b3f0bbdeaff.PNG" height="400">

Cm-Alpha grafiği Model vs. Referans

<img src="https://user-images.githubusercontent.com/47147130/125116874-08413580-e0f6-11eb-830d-1895e4e60d9f.png" height="400"><img src="https://user-images.githubusercontent.com/47147130/125116890-11ca9d80-e0f6-11eb-9f87-fc7fedc617ac.PNG" height="400">


Cm-Beta grafiği Model vs. Referans

<img src="https://user-images.githubusercontent.com/47147130/125116941-25760400-e0f6-11eb-9b23-0e932d4d9a29.png" height="400"><img src="https://user-images.githubusercontent.com/47147130/125116967-2e66d580-e0f6-11eb-8cd9-431e68c30c2f.PNG" height="400">





