import cv2

# Abre a câmera
cap = cv2.VideoCapture(0)

while True:
    # Lê o frame da câmera
    ret, frame = cap.read()

    # Exibe o frame
    cv2.imshow('Camera', frame)

    # Aguarda a tecla 'q' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()

