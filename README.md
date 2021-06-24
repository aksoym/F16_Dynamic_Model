# F16_Dynamic_Model

## Yapılacaklar:

- Cm-alpha, CL-alpha vb. grafiklerini gösteren fonksiyonlar (monitoring tools) yazılacak. 
- LQR ile SAS kurgusu yazılacak, amaç Cm-alpha, CL vb. gibi değerleri stabil bölgeden çıkartacak manevralara, karşı manevra oluşturacak (elevator, aileron, rudder, thrust)
kontrol girdilerini kontrolcüye verdirmek.
- Aerodinamik model polinom temelden deneysel veri temeline geçecek. '.mat' uzantılı dosya şeklinde aerodinamik datalar mevcut, bunları uygun biçimde parse edebilmek gerekli.
- Son olarak yazılan modellerin/kodun genel olarak (aero_model, propulsion_model gibi) nesne tabanlı hale (class objelerine) dönüştürülmesi. Örneğin Aero_model diye bir class 
oluşturulması ve 'get_aero_forces', 'get_aero_moments' fonksiyonlarının bu class'ın metodu haline getirilmesi.
