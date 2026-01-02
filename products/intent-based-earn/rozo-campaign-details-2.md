# Documento de Reglas de Incentivos de la Campaña ROZO Earn

> Versión: v9.0
> Actualizado: 2026/01/03
> El protocolo proporciona el rendimiento, ROZO proporciona equidad, participación y crecimiento.

---

## 1. Resumen de la Campaña

| Elemento | Detalles |
|----------|----------|
| Nombre de la Campaña | Programa de Incentivos ROZO Earn Enero |
| Pool de Premios Total | $10,000 Subsidio ROZO |
| Rendimiento del Protocolo | 15% APY (Protocolo Nativo) |
| Cadenas Soportadas | Solana / Base |
| Duración de la Campaña | 5 Semanas (5 Competencias Semanales Independientes, Puntos se Reinician Semanalmente) |

### Puntos Destacados

- **Rendimiento del Protocolo**: 15% APY, depósitos ilimitados, comienza a ganar instantáneamente
- **Cash Back**: Recompensas en tiempo real (Bridge: reembolso 2x de comisiones, Pagos: 1%-20%)
- **ROZO Garantiza Equidad**: Puntuación con raíz cuadrada √n previene dominio de ballenas
- **Todos Pueden Ganar**: Tabla de clasificación + Sorteo, recompensas para todos
- **Barrera Ultra Baja**: Comienza con solo $1, tareas para principiantes fáciles de completar

---

## 2. Sistema de Incentivos de Doble Vía

ROZO utiliza un sistema de incentivos de doble vía **Cash Back + Puntos**:

| Sistema | Propósito | Cálculo | Distribución |
|---------|-----------|---------|--------------|
| **Cash Back** | Recompensas Instantáneas (Garantizadas) | Basado en tipo de transacción | Tiempo real |
| **Puntos** | Tabla de Clasificación + Sorteo (Competencia Gamificada) | √(Saldo) + Puntos de Tareas | Snapshot Diario |

```
Vista de Interfaz del Usuario:
┌─────────────────────────┐
│  Cash Back: $0.50       │  ← Recompensas de Transacción
│  Puntos: 156 pts        │  ← Para Clasificación/Sorteo
│  Ranking: #42           │
└─────────────────────────┘
```

### ¿Por Qué Dos Sistemas Separados?

1. **Separación de Cuentas Mentales**: Cash Back = "Dinero garantizado en el bolsillo", Puntos = "Competencia gamificada"
2. **Doble Motivación**: Satisfacción al depositar (cashback), satisfacción al mantener (puntos crecen)
3. **Menor Carga Cognitiva**: Cash Back = Dinero, Puntos = Puntuación, sin confusión

---

## 3. Mecanismo de Cash Back

### Reglas

| Tipo de Transacción | Cálculo de Cash Back | Descripción |
|---------------------|---------------------|-------------|
| **Bridge (Cross-chain)** | Comisión × 2 | Reembolso doble en comisiones cross-chain |
| **Pago** | 1% - 20% | Tasa específica de cashback mostrada en página del comerciante antes del pago |

### Características

- **Tiempo Real**: Acreditado inmediatamente tras transacción exitosa
- **Retirable**: Cash Back va directamente al saldo, retira cuando quieras
- **Independiente**: Cash Back y Puntos se calculan por separado

---

## 4. Sistema de Puntos

### Fórmula Principal

```
Puntos Diarios = √(Saldo Mínimo en Snapshot UTC 00:00)
```

**Monto Mínimo de Participación: $1 USDC** (o €1 EU)

### Tabla de Referencia de Puntos

| Monto de Depósito | Puntos Diarios |
|-------------------|----------------|
| $1 | 1 punto |
| $10 | 3.16 puntos |
| $50 | 7.07 puntos |
| $100 | 10 puntos |
| $500 | 22.4 puntos |
| $1,000 | 31.6 puntos |
| $5,000 | 70.7 puntos |
| $10,000 | 100 puntos (límite de cálculo) |

### Explicación del Ciclo de Puntos

**Importante: Campaña de 5 Semanas = 5 Competencias Semanales Independientes, ¡Los Puntos NO se Acumulan!**

| Tipo de Punto | Ciclo | Descripción |
|---------------|-------|-------------|
| **Tareas Únicas** (Primer depósito, vinculación, etc.) | Solo una vez | Reclamado en Semana 1, no disponible después |
| **Puntos de Saldo Diario** | Recalculado semanalmente | Se reinicia a cero cada semana |
| **Bonificación por Referidos** | Recalculado semanalmente | Sigue los puntos semanales |

**Ejemplo**:
- Semana 1: Puntos de Saldo + Tareas Únicas + Referidos = **Puntuación Alta** (Bonus de usuario nuevo)
- Semana 2+: Solo Puntos de Saldo + Referidos = **Puntuación Menor** (Depósitos sostenidos)

---

## 5. Sistema de Tareas para Principiantes (Simple y Fácil)

### A. Tareas Únicas (Solo se Pueden Reclamar Una Vez)

| Tarea | Puntos | Condición |
|-------|--------|-----------|
| Primer Depósito | **+20 pts** | Depósito ≥ $1 |
| Vincular Twitter | +15 pts | Autorización OAuth |
| Vincular Discord | +15 pts | Autorización OAuth |
| Primer Referido Exitoso | +20 pts | Invitar 1 persona que deposite ≥ $1 |

**Total de Bonificación por Tareas Únicas: Hasta 70 puntos**

### B. Tareas Diarias (Recalculadas Semanalmente)

| Tarea | Cálculo de Puntos | Frecuencia | Condición |
|-------|-------------------|------------|-----------|
| Puntos de Saldo | √(Saldo Mínimo Diario) | Snapshot Diario | Saldo ≥ $1 |

**Regla Importante**: Los puntos diarios se calculan basándose en el **saldo mínimo del día** (previene depósitos flash).

### C. Bonificación por Referidos (Recalculada Semanalmente)

| Tipo | Bonificación | Condición |
|------|--------------|-----------|
| Referido Nivel-1 | +20% | Usuario referido deposita ≥ $1 |

**Fórmula de Bonificación por Referidos**:
```
Bonificación por Referidos = Σ(Puntos de Saldo del Usuario Referido × 20%)
```

**Notas**:
- Solo cuenta los **puntos de saldo** del usuario referido, no puntos de tareas únicas
- Basado en los puntos semanales reales del usuario referido, recalculado semanalmente

**Reglas de Límite**:
- Si tienes depósitos: Límite = Tus propios puntos
- Si no tienes depósitos: Límite = 100 puntos

**Ejemplo**:
- Usuario A (sin depósitos) refiere al nuevo Usuario B (depósito de $50, 49.49 puntos de saldo)
- Bonificación de referido de A = min(49.49 × 20%, 100) = **9.9 puntos**
- Si A refiere 10 personas (cada una con 50 puntos de saldo), teórico 100 pts, límite real **100 puntos**

---

## 6. Mecanismo de Recompensas por Puntos

### Pool de Premios Semanal de $1,500

```
Pool de Premios Semanal $1,500
├── Tabla de Clasificación Top 30: $1,000 (Por ranking de puntos)
└── Sorteo 20 Ganadores: $500 (Usuarios fuera del Top 30)
```

### 6.1 Recompensas de Tabla de Clasificación ($1,000/semana)

| Ranking | Recompensa |
|---------|------------|
| 1 | $150 |
| 2 | $100 |
| 3 | $80 |
| 4-10 | $50 cada uno ($350) |
| 11-20 | $20 cada uno ($200) |
| 21-30 | $12 cada uno ($120) |

**Sin Umbral**: Todos los usuarios clasificados por puntos, las puntuaciones más altas entran al Top 30.

### 6.2 Sorteo de la Suerte ($500/semana)

| Elemento | Detalles |
|----------|----------|
| Pool de Premios | $500/semana |
| Ganadores | 20 personas |
| Premio por Ganador | $25 |

**Condiciones del Sorteo**:
- No estar en el Top 30 de la tabla de clasificación
- Debe tener puntos para participar

**Reglas del Sorteo**: Lotería ponderada, más puntos = mayor probabilidad de ganar.

---

## 7. Tabla de Referencia Rápida

### Reglas de Cash Back

| Regla | Valor |
|-------|-------|
| Cashback de Bridge | Comisión × 2 |
| Cashback de Pago | 1% - 20% |
| Distribución | Tiempo real |

### Reglas de Puntos

| Regla | Valor |
|-------|-------|
| Depósito Mínimo Válido | **$1** |
| Límite de Saldo para Cálculo de Puntos | $10,000 |
| Umbral de Referido Válido | Usuario referido deposita ≥ $1 |
| Límite de Bonificación por Referido (Con Depósito) | No puede exceder tus propios puntos |
| Límite de Bonificación por Referido (Sin Depósito) | 100 puntos |
| Hora del Snapshot Diario | UTC 00:00 |
| Ciclo de Puntos | Reinicio semanal (excepto tareas únicas) |
| Hora de Anuncio del Sorteo | Lunes 00:00 UTC (Singapur/HK 08:00 / Londres 00:00 / LA Domingo 16:00) |

---

## 8. Ejemplos de Ganancias de Usuario

### Usuario Nuevo Semana 1 (Depósito $100)

| Fuente de Ganancias | Monto/Puntos |
|---------------------|--------------|
| **Cash Back** | Basado en tipo de transacción |
| Rendimiento del Protocolo (15% APY) | ~$0.29/semana |
| Puntos de Saldo Diario | 10 × 7 = 70 pts |
| Tareas Únicas | +70 pts (Primer depósito + vinculaciones, etc.) |
| **Puntos Totales Semanales** | **140 pts** |

### Usuario Recurrente Semana 2 (Mismo $100)

| Fuente de Ganancias | Monto/Puntos |
|---------------------|--------------|
| Rendimiento del Protocolo (15% APY) | ~$0.29/semana |
| Puntos de Saldo Diario | 10 × 7 = 70 pts |
| Tareas Únicas | 0 (Ya reclamado) |
| **Puntos Totales Semanales** | **70 pts** |

### Usuario Solo Referidos (Sin Depósito, Refiere 5 Nuevos Usuarios)

| Fuente de Ganancias | Puntos |
|---------------------|--------|
| Propios Puntos de Saldo | 0 pts |
| Bonificación por Referidos (5 × 50 × 20%) | Teórico 50 pts |
| Real | **50 pts** |

*Nota: La bonificación por referidos solo cuenta los puntos de saldo de los usuarios referidos, no las tareas únicas*

### Comparación Usuario Nuevo vs. Recurrente

Usuario nuevo deposita $10 (una semana): 22 + 70 = **92 pts**
Usuario recurrente necesita igualar: **$173** (√173 × 7 ≈ 92)

---

## 9. Mecanismos Anti-Abuso

| Capa | Mecanismo | Efecto |
|------|-----------|--------|
| Registro | Vinculación de dispositivo Passkey | Alto costo para registro masivo |
| Puntos | Fórmula de raíz cuadrada √n | Dividir cuentas reduce retornos |
| Snapshot | Usa saldo mínimo diario | Previene farming de depósitos flash |
| Límite | Límite de cálculo de puntos $10,000 | Retornos decrecientes para ballenas |
| Referidos | Bonificación limitada a tus propios puntos | Previene esquemas piramidales infinitos |

---

*Versión del Documento: v9.0*
*Última Actualización: 2026/01/03*
