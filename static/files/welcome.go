// Пакет отримано, але його вміст замаскований.
// Знайдіть, як відновити початковий текст. Шукати ключ поза цим файлом не потрібно.
package main

import "fmt"

const mask byte = 0x2a

var packet = []byte{0x63, 0x69, 0x6f, 0x51, 0x5d, 0x4f, 0x46, 0x49, 0x45, 0x47, 0x4f, 0x75, 0x5e, 0x45, 0x75, 0x49, 0x53, 0x48, 0x4f, 0x58, 0x75, 0x43, 0x49, 0x4f, 0x75, 0x48, 0x45, 0x52, 0x57}

func restore(data []byte) string {
	restored := make([]byte, len(data))
	for i, value := range data {
		restored[i] = value ^ mask
	}
	return string(restored)
}

func main() {
	fmt.Printf("Отримано %d байтів. Функція restore допоможе прочитати пакет.\n", len(packet))
}
