# [Borrador] Reglas de Cálculo de Puntos ROZO Earn y Simulaciones de Usuario

> Versión: v4.0
> Actualizado: 2026/01/03

---

## 1. Sistema de Incentivos de Doble Vía

| Sistema | Propósito | Cálculo | Distribución |
|---------|-----------|---------|--------------|
| **Cash Back** | Recompensas Instantáneas | Bridge: Comisión×2 / Pago: 1%-20% | Tiempo real |
| **Puntos** | Clasificación + Sorteo | √(Saldo) + Puntos de Tareas + Bonificación por Referidos | Snapshot Diario |

---

## 2. Fórmula de Cálculo de Puntos

### Fórmula de Puntos Totales

```
Puntos Totales Semanales = Σ(Diario √Saldo) + Puntos de Tareas Únicas + Bonificación por Referidos
```

### 1. Puntos Base Diarios (Principal)

```
Puntos Diarios = √(Saldo Mínimo Diario)
```

| Saldo | Puntos Diarios |
|-------|----------------|
| $1 | 1.00 |
| $5 | 2.24 |
| $10 | 3.16 |
| $25 | 5.00 |
| $50 | 7.07 |
| $100 | 10.00 |
| $200 | 14.14 |
| $500 | 22.36 |
| $1,000 | 31.62 |
| $2,000 | 44.72 |
| $5,000 | 70.71 |
| $10,000 | 100.00 (límite) |

### 2. Puntos de Tareas Únicas

| Tarea | Puntos | Condición de Activación |
|-------|--------|-------------------------|
| Primer Depósito | +20 | Depósito ≥ $1 |
| Vincular Twitter | +15 | Completar Autorización OAuth |
| Vincular Discord | +15 | Completar Autorización OAuth |
| Primer Referido Exitoso | +20 | Invitar 1 persona a depositar ≥ $1 |

**Máximo de Puntos por Tareas Únicas: 70**

### 3. Bonificación por Referidos

```
Bonificación por Referidos = Σ(Puntos de Saldo del Usuario Referido × 20%)
```

**Notas**:
- Solo cuenta los **puntos de saldo** del usuario referido, no puntos de tareas únicas
- Basado en los puntos semanales reales del usuario referido, recalculado semanalmente

**Reglas de Límite**:
- Si tienes depósitos: Límite = Tus propios puntos
- Si no tienes depósitos: Límite = 100 puntos

---

## 3. Explicación del Ciclo de Puntos

**Importante: Campaña de 5 Semanas = 5 Competencias Semanales Independientes, ¡Los Puntos NO se Acumulan!**

| Tipo de Punto | Ciclo | Descripción |
|---------------|-------|-------------|
| **Tareas Únicas** | Solo una vez | Reclamado en Semana 1, no disponible después |
| **Puntos de Saldo Diario** | Recalculado semanalmente | Se reinicia a cero cada semana |
| **Bonificación por Referidos** | Recalculado semanalmente | Sigue los puntos semanales |

**Hora de Anuncio del Sorteo**: Cada Lunes 00:00 UTC
- Singapur/Hong Kong: Lunes 08:00
- Londres: Lunes 00:00
- Los Ángeles: Domingo 16:00

---

## 4. Ejemplos de Simulación de Usuario

### Usuario A: Principiante Nuevo (Deposita $50, Completa Tareas)

**Contexto**: Estudiante, deposita $50, completa todas las tareas simples

#### Registro de Actividad

| Día | Acción | Saldo | Puntos Diarios |
|-----|--------|-------|----------------|
| Día 1 | Depositar $50, Vincular Twitter | $50 | √50 = 7.07 |
| Día 2 | Vincular Discord | $50 | 7.07 |
| Día 3 | Referir exitosamente al Amigo B | $50 | 7.07 |
| Día 4 | Sin acción | $50 | 7.07 |
| Día 5 | Sin acción | $50 | 7.07 |
| Día 6 | Sin acción | $50 | 7.07 |
| Día 7 | Sin acción | $50 | 7.07 |

#### Cálculo de Puntos

```
Puntos de Saldo Diario: 7.07 × 7 = 49.49 pts

Tareas Únicas:
  - Primer Depósito: +20
  - Vincular Twitter: +15
  - Vincular Discord: +15
  - Primer Referido Exitoso: +20
  Subtotal: +70 pts

Bonificación por Referido: Puntos de saldo del Amigo B 49.49 × 20% = 9.9 pts
  (Nota: Solo cuenta puntos de saldo, no tareas únicas)

───────────────────────────
Puntos Totales Semanales: 49.49 + 70 + 9.9 = 129.39 pts
```

**Resultado**: ¡Elegible para sorteo semanal, oportunidad de ganar $25!

---

### Usuario B: Usuario Regular (Deposita $500, Refiere 2 Personas)

**Contexto**: Oficinista, deposita $500, referido por A, también refiere 2 personas

#### Registro de Actividad

| Día | Acción | Saldo | Puntos Diarios |
|-----|--------|-------|----------------|
| Día 1 | Depositar $500 vía enlace de A | $500 | √500 = 22.36 |
| Día 2 | Vincular Twitter + Discord | $500 | 22.36 |
| Día 3 | Referir Amigo C ($100) | $500 | 22.36 |
| Día 4 | Referir Amigo D ($50) | $500 | 22.36 |
| Día 5 | Sin acción | $500 | 22.36 |
| Día 6 | Sin acción | $500 | 22.36 |
| Día 7 | Sin acción | $500 | 22.36 |

#### Cálculo de Puntos

```
Puntos de Saldo Diario: 22.36 × 7 = 156.52 pts

Tareas Únicas:
  - Primer Depósito: +20
  - Vincular Twitter: +15
  - Vincular Discord: +15
  - Primer Referido Exitoso: +20
  Subtotal: +70 pts

Bonificación por Referido (solo puntos de saldo):
  - Amigo C ($100) puntos de saldo 70 × 20% = 14 pts
  - Amigo D ($50) puntos de saldo 49.49 × 20% = 9.9 pts
  Subtotal: 23.9 pts

───────────────────────────
Puntos Totales Semanales: 156.52 + 70 + 23.9 = 250.42 pts
```

**Resultado**: ¡Buena oportunidad de entrar al Top 30 de la clasificación!

---

### Usuario C: Usuario Ballena (Deposita $5,000, Apunta al Top)

**Contexto**: Veterano de DeFi, deposita $5,000, enfocado en rendimiento + ranking

#### Registro de Actividad

| Día | Acción | Saldo | Puntos Diarios |
|-----|--------|-------|----------------|
| Día 1 | Depositar $5,000 | $5,000 | √5000 = 70.71 |
| Día 2 | Vincular Twitter + Discord | $5,000 | 70.71 |
| Día 3 | Referir 5 amigos | $5,000 | 70.71 |
| Día 4 | Sin acción | $5,000 | 70.71 |
| Día 5 | Sin acción | $5,000 | 70.71 |
| Día 6 | Sin acción | $5,000 | 70.71 |
| Día 7 | Sin acción | $5,000 | 70.71 |

#### Cálculo de Puntos

```
Puntos de Saldo Diario: 70.71 × 7 = 494.97 pts

Tareas Únicas:
  - Primer Depósito: +20
  - Vincular Twitter: +15
  - Vincular Discord: +15
  - Primer Referido Exitoso: +20
  Subtotal: +70 pts

Bonificación por Referido (solo puntos de saldo):
  - 5 amigos, asumiendo cada uno tiene 70 puntos de saldo
  - Bonificación teórica: 70 × 20% × 5 = 70 pts
  - Verificación de límite: min(70, 494.97+70) = 70 pts

───────────────────────────
Puntos Totales Semanales: 494.97 + 70 + 70 = 634.97 pts
```

**Resultado**: ¡Garantizado Top 10, fuerte contendiente para Top 3!

---

### Usuario D: Referidor Puro (Sin Depósitos, Solo Referidos)

**Contexto**: KOL, no deposita, pero refiere muchas personas

#### Cálculo de Puntos

```
Propios Puntos de Saldo: 0 pts (sin depósitos)

Bonificación por Referido (solo puntos de saldo):
  - Refirió 10 nuevos usuarios, cada uno con ~50 puntos de saldo
  - Bonificación teórica: 50 × 20% × 10 = 100 pts
  - Verificación de límite (sin depósitos, límite = 100): min(100, 100) = 100 pts

───────────────────────────
Puntos Totales Semanales: 0 + 0 + 100 = 100 pts
```

**Resultado**: ¡Referidores puros pueden ganar máx 100 puntos, elegibles para sorteo!

*Nota: La bonificación por referidos solo cuenta los puntos de saldo de usuarios referidos, no tareas únicas*

---

## 5. Comparación Usuario Nuevo vs. Recurrente

| Tipo de Usuario | Depósito | Puntos Semanales | Notas |
|-----------------|----------|------------------|-------|
| Usuario Nuevo | $10 | 22 + 70 = **92 pts** | Tiene bonificación de tareas únicas |
| Usuario Recurrente (para igualar) | **$173** | 92 pts | Solo puntos de saldo |

Usuario nuevo con $10 = Usuario recurrente con $173 (desde Semana 2)

---

## 6. Comparación de Estrategias

| Usuario | Depósito | Puntos Semanales | Objetivo | Recompensa Esperada | Cómo Ganar |
|---------|----------|------------------|----------|---------------------|------------|
| A | $50 | ~129 pts | Sorteo | $25 | Probabilidad (más puntos = mejores chances) |
| B | $500 | ~250 pts | Top 30 | $12-50 | **Garantizado** (por ranking) |
| C | $5,000 | ~635 pts | Top 3 | $80-150 | **Garantizado** (por ranking) |
| D | $0 (solo referidos) | 100 pts | Sorteo | $25 | Probabilidad (más puntos = mejores chances) |

### Observaciones Clave

1. **Pequeños Depositantes**: Dependen de puntos de tareas + sorteo, baja inversión pero tienen oportunidades
2. **Depositantes Medianos**: Tareas + referidos juntos, mejor valor por esfuerzo
3. **Grandes Depositantes**: Puntos de saldo dominan, pero fórmula √n limita ventaja de ballenas
4. **Referidores Puros**: Máximo 100 puntos, fomenta participación pero previene arbitraje puro

---

## 7. Hoja de Ruta de Inicio Rápido

### Lista de Tareas Primera Semana para Principiantes

- [ ] Día 1: Depositar $1 o más (Ganar +20 puntos de primer depósito)
- [ ] Día 1: Vincular Twitter (+15)
- [ ] Día 1: Vincular Discord (+15)
- [ ] Día 2: Referir exitosamente 1 amigo (+20)
- [ ] Día 3-7: Mantener saldo, no retirar

**Puntos Esperados**: ~90-140 pts (dependiendo del monto del depósito)

---

*Versión del Documento: v4.0*
*Última Actualización: 2026/01/03*
