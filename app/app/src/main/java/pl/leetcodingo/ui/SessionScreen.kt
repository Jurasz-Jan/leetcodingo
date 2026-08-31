package pl.leetcodingo.ui

import androidx.activity.compose.BackHandler
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.calculateZoom
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import pl.leetcodingo.data.Answer
import pl.leetcodingo.data.Exercise
import pl.leetcodingo.data.Streak
import pl.leetcodingo.session.SessionViewModel
import pl.leetcodingo.session.Topic
import pl.leetcodingo.session.UiState
import kotlin.math.cos
import kotlin.math.sin
import kotlin.random.Random

@Composable
fun SessionScreen(viewModel: SessionViewModel) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    Scaffold { insets ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(insets),
            contentAlignment = Alignment.Center,
        ) {
            when (val current = state) {
                UiState.Loading -> CircularProgressIndicator()

                is UiState.Failed -> Text(
                    text = current.message,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(24.dp),
                )

                is UiState.Menu -> MenuScreen(
                    state = current,
                    onMixed = viewModel::startMixed,
                    onTopic = viewModel::startTopic,
                )

                is UiState.Running -> {
                    BackHandler(onBack = viewModel::openMenu)
                    RunningScreen(
                        state = current,
                        onPick = viewModel::pick,
                        onSubmit = viewModel::submit,
                        onNext = viewModel::next,
                        onMenu = viewModel::openMenu,
                    )
                }

                is UiState.Finished -> {
                    BackHandler(onBack = viewModel::openMenu)
                    FinishedScreen(
                        state = current,
                        onAgain = viewModel::again,
                        onMenu = viewModel::openMenu,
                    )
                }
            }
        }
    }
}

@Composable
private fun MenuScreen(
    state: UiState.Menu,
    onMixed: () -> Unit,
    onTopic: (String) -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = 24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text(text = "leetcodingo", style = MaterialTheme.typography.headlineSmall)
        Text(
            text = "${state.total} ćwiczeń, w tym ${state.unseen} jeszcze niewidzianych",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        StreakLine(state.streak)

        Spacer(Modifier.height(4.dp))

        Button(onClick = onMixed, modifier = Modifier.fillMaxWidth()) {
            Text("Sesja mieszana")
        }
        Text(
            text = "Trzy minuty z całego korpusu, nowe ćwiczenia najpierw.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )

        Spacer(Modifier.height(8.dp))

        Text(text = "Sesja tematyczna", style = MaterialTheme.typography.titleMedium)
        Text(
            text = "Jeden wzorzec na całą sesję. Przy każdym temacie liczba ćwiczeń, a po kropce te jeszcze niewidziane.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )

        Spacer(Modifier.height(4.dp))

        state.topics.forEach { topic ->
            TopicRow(topic = topic, onClick = { onTopic(topic.pattern) })
        }
    }
}

@Composable
private fun TopicRow(topic: Topic, onClick: () -> Unit) {
    // Wyczerpany temat zostaje klikalny: powtórka jest wtedy sensownym wyborem,
    // tylko nie ma już w nim nic nowego i lepiej to widzieć przed wejściem.
    val exhausted = topic.unseen == 0

    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .border(
                width = 1.dp,
                color = MaterialTheme.colorScheme.outlineVariant,
                shape = RoundedCornerShape(8.dp),
            )
            .clickable(onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 12.dp),
    ) {
        Text(
            text = topic.pattern,
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.weight(1f),
        )
        Text(
            text = when {
                exhausted -> "${topic.total}  ·  wszystko widziane"
                // Przy nietkniętym temacie obie liczby są równe i powtarzanie ich
                // niczego nie wnosi.
                topic.unseen == topic.total -> "${topic.total}"
                else -> "${topic.total}  ·  ${topic.unseen} nowych"
            },
            style = MaterialTheme.typography.labelMedium,
            color = if (exhausted) {
                MaterialTheme.colorScheme.onSurfaceVariant
            } else {
                MaterialTheme.colorScheme.primary
            },
        )
    }
}

@Composable
private fun RunningScreen(
    state: UiState.Running,
    onPick: (Int) -> Unit,
    onSubmit: () -> Unit,
    onNext: () -> Unit,
    onMenu: () -> Unit,
) {
    val exercise = state.exercise
    val scroll = rememberScrollState()

    // Skala kodu żyje na poziomie ekranu, nie pojedynczego ćwiczenia: raz powiększony
    // kod zostaje powiększony na kolejnych zadaniach i po obrocie ekranu.
    var codeScale by rememberSaveable { mutableFloatStateOf(1f) }

    // Wyjasnienie dopisuje sie na koncu kolumny, wiec bez tego konczy sie tuz pod
    // krawedzia ekranu i wyglada na uciete w pol zdania.
    LaunchedEffect(exercise.id, state.revealed) {
        if (state.revealed) scroll.animateScrollTo(scroll.maxValue) else scroll.scrollTo(0)
    }

    Column(modifier = Modifier.fillMaxSize()) {
        LinearProgressIndicator(
            progress = { state.position.toFloat() / state.total },
            modifier = Modifier.fillMaxWidth(),
        )

        Column(
            modifier = Modifier
                .weight(1f)
                .verticalScroll(scroll)
                .padding(horizontal = 20.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                // Przy `recognize-pattern` nazwa wzorca JEST odpowiedzią, więc nie może
                // stać w nagłówku nad pytaniem. Pokazujemy ją dopiero po odsłonięciu.
                val showPattern = exercise.type != "recognize-pattern" || state.revealed
                Text(
                    text = buildString {
                        append("${state.position}/${state.total}")
                        // Trafienia dopiero od drugiego zadania: przy pierwszym
                        // pokazywalyby zawsze zero i tylko zajmowaly miejsce.
                        if (state.position > 1) append("  ·  ${state.correctSoFar} trafione")
                        if (showPattern) append("  ·  ${exercise.pattern}")
                        append("  ·  trudność ${exercise.difficulty}")
                    },
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.weight(1f),
                )
                TextButton(onClick = onMenu) { Text("Menu") }
            }

            SpecCard(spec = exercise.spec, withCode = exercise.code.isNotBlank())

            Text(text = exercise.prompt, style = MaterialTheme.typography.titleMedium)

            if (exercise.code.isNotBlank()) {
                CodeBlock(
                    code = exercise.code,
                    scale = codeScale,
                    onScaleChange = { codeScale = it },
                )
            }

            exercise.options.forEachIndexed { index, option ->
                OptionRow(
                    text = option,
                    monospace = exercise.type in MONOSPACE_TYPES,
                    order = state.picked.indexOf(index).takeIf { it >= 0 }?.plus(1),
                    ordering = exercise.answer is Answer.Ordering,
                    selected = index in state.picked,
                    state = optionState(exercise, state, index),
                    onClick = { onPick(index) },
                )
            }

            if (state.revealed) {
                ExplanationCard(exercise, state.isCorrect)
            }
        }

        Column(modifier = Modifier.padding(horizontal = 20.dp, vertical = 12.dp)) {
            // Wyszarzony przycisk bez wyjasnienia wyglada jak zepsuty, a przy ukladaniu
            // kolejnosci trzeba ustawic wszystkie kroki, zanim da sie sprawdzic.
            if (!state.revealed && !state.canSubmit) {
                Text(
                    text = if (exercise.answer is Answer.Ordering) {
                        "Ustaw wszystkie ${exercise.options.size} kroków, stukając w nie po kolei."
                    } else {
                        "Wybierz jedną z odpowiedzi."
                    },
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(bottom = 8.dp),
                )
            }
            Button(
                onClick = if (state.revealed) onNext else onSubmit,
                enabled = state.revealed || state.canSubmit,
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text(if (state.revealed) "Dalej" else "Sprawdź")
            }
        }
    }
}

private enum class OptionState { NEUTRAL, CORRECT, WRONG }

/**
 * Typy, w ktorych opcje sa kodem albo danymi wejsciowymi. Tylko one dostaja czcionke
 * o stalej szerokosci; zdania po polsku czyta sie w niej gorzej, a takich opcji jest
 * w korpusie wiekszosc.
 */
private val MONOSPACE_TYPES = setOf("find-bug", "fill-gap", "predict-output", "complexity")

private const val CODE_BASE_SP = 11f
private const val CODE_SCALE_MIN = 0.8f
private const val CODE_SCALE_MAX = 2.5f

private fun optionState(exercise: Exercise, state: UiState.Running, index: Int): OptionState {
    if (!state.revealed) return OptionState.NEUTRAL
    return when (val answer = exercise.answer) {
        is Answer.Choice -> when {
            index == answer.index -> OptionState.CORRECT
            index in state.picked -> OptionState.WRONG
            else -> OptionState.NEUTRAL
        }

        is Answer.Ordering -> when {
            state.isCorrect -> OptionState.CORRECT
            state.picked.indexOf(index) == answer.order.indexOf(index) -> OptionState.CORRECT
            else -> OptionState.WRONG
        }
    }
}

/**
 * Naglowek zalezy od tego, czy cwiczenie w ogole pokazuje kod. Przy 157 z 214 cwiczen
 * zadnego kodu nie ma i „co kod ma robic" jest wtedy po prostu nieprawda.
 */
@Composable
private fun SpecCard(spec: String, withCode: Boolean) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant,
        ),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(
                text = if (withCode) "CO KOD MA ROBIĆ" else "ZADANIE",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(Modifier.height(4.dp))
            Text(text = spec, style = MaterialTheme.typography.bodyMedium)
        }
    }
}

/**
 * Kod zawija sie zamiast przewijac w poziomie, bo zmutowana linia nie moze wyladowac
 * poza ekranem: cwiczenie polega wlasnie na jej zauwazeniu.
 *
 * Skalowanie reaguje wylacznie na dwa palce. Gest jednopalcowy nie jest konsumowany,
 * dzieki czemu przewijanie calej strony dziala normalnie takze nad blokiem kodu.
 */
@Composable
private fun CodeBlock(code: String, scale: Float, onScaleChange: (Float) -> Unit) {
    Surface(
        color = MaterialTheme.colorScheme.surfaceContainerHighest,
        shape = RoundedCornerShape(8.dp),
        modifier = Modifier
            .fillMaxWidth()
            .pointerInput(Unit) {
                awaitEachGesture {
                    awaitFirstDown(requireUnconsumed = false)
                    do {
                        val event = awaitPointerEvent()
                        if (event.changes.size >= 2) {
                            val zoom = event.calculateZoom()
                            if (zoom != 1f) {
                                onScaleChange(
                                    (scale * zoom).coerceIn(CODE_SCALE_MIN, CODE_SCALE_MAX)
                                )
                                event.changes.forEach { it.consume() }
                            }
                        }
                    } while (event.changes.any { it.pressed })
                }
            },
    ) {
        Text(
            text = code,
            fontFamily = FontFamily.Monospace,
            fontSize = (CODE_BASE_SP * scale).sp,
            lineHeight = (CODE_BASE_SP * scale * 1.55f).sp,
            modifier = Modifier.padding(12.dp),
        )
    }
}

@Composable
private fun OptionRow(
    text: String,
    monospace: Boolean,
    order: Int?,
    ordering: Boolean,
    selected: Boolean,
    state: OptionState,
    onClick: () -> Unit,
) {
    val border = when (state) {
        OptionState.CORRECT -> Color(0xFF2E7D32)
        OptionState.WRONG -> MaterialTheme.colorScheme.error
        OptionState.NEUTRAL ->
            if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant
    }

    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier
            .fillMaxWidth()
            .border(1.5.dp, border, RoundedCornerShape(8.dp))
            .clickable(onClick = onClick)
            .padding(12.dp),
    ) {
        if (ordering) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(24.dp)
                    .background(
                        if (order != null) MaterialTheme.colorScheme.primary else Color.Transparent,
                        CircleShape,
                    )
                    .border(1.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape),
            ) {
                if (order != null) {
                    Text(
                        text = order.toString(),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onPrimary,
                    )
                }
            }
        }
        Text(
            text = text,
            fontFamily = if (monospace) FontFamily.Monospace else FontFamily.Default,
            style = if (monospace) {
                MaterialTheme.typography.bodySmall
            } else {
                MaterialTheme.typography.bodyMedium
            },
        )
    }
}

@Composable
private fun ExplanationCard(exercise: Exercise, correct: Boolean) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(14.dp)) {
            Text(
                text = if (correct) "Dobrze" else "Źle",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                color = if (correct) Color(0xFF2E7D32) else MaterialTheme.colorScheme.error,
            )
            Spacer(Modifier.height(6.dp))
            Text(text = exercise.explanation, style = MaterialTheme.typography.bodyMedium)
            exercise.specRef?.let { ref ->
                Spacer(Modifier.height(8.dp))
                Text(
                    text = "ze specyfikacji: „$ref”",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun StreakLine(streak: Streak) {
    val text = when {
        streak.days == 0 -> "Brak serii. Dokończona sesja dzisiaj ją zaczyna."
        streak.days == 1 -> "Seria: 1 dzień"
        streak.days in 2..4 -> "Seria: ${streak.days} dni"
        else -> "Seria: ${streak.days} dni  ·  rekord ${streak.best}"
    }
    Text(
        text = text,
        style = MaterialTheme.typography.labelLarge,
        color = if (streak.days == 0) {
            MaterialTheme.colorScheme.onSurfaceVariant
        } else {
            MaterialTheme.colorScheme.primary
        },
    )
}

/** Jeden kawałek konfetti: kierunek, prędkość i obrót losowane raz, przy pierwszym rysowaniu. */
private data class Confetto(
    val angleRadians: Float,
    val speed: Float,
    val spin: Float,
    val color: Color,
    val width: Float,
    val height: Float,
)

private val CONFETTI_COLORS = listOf(
    Color(0xFF2E7D32),
    Color(0xFF1565C0),
    Color(0xFFF9A825),
    Color(0xFFC62828),
    Color(0xFF6A1B9A),
)

/**
 * Wybuch konfetti nad liczbą dni serii.
 *
 * Rysowany na Canvasie, bez zewnętrznych bibliotek. Tor każdego kawałka to rzut ukośny:
 * stała prędkość początkowa plus przyspieszenie w dół, więc cząstki najpierw wystrzeliwują
 * w górę, a potem opadają. Przezroczystość gaśnie na ostatniej ćwiartce animacji, żeby
 * konfetti znikało samo, zamiast urywać się w połowie ekranu.
 */
@Composable
private fun StreakCelebration(streak: Streak) {
    val confetti = remember {
        List(32) {
            val spread = Random.nextFloat() * 2.2f - 1.1f
            Confetto(
                // -90 stopni to prosto w gore; rozrzut na boki daje ksztalt wachlarza.
                angleRadians = (-Math.PI / 2).toFloat() + spread,
                speed = 420f + Random.nextFloat() * 620f,
                spin = -10f + Random.nextFloat() * 20f,
                color = CONFETTI_COLORS[Random.nextInt(CONFETTI_COLORS.size)],
                width = 10f + Random.nextFloat() * 10f,
                height = 5f + Random.nextFloat() * 6f,
            )
        }
    }

    val progress = remember { Animatable(0f) }
    LaunchedEffect(streak.days) {
        progress.snapTo(0f)
        progress.animateTo(1f, animationSpec = tween(durationMillis = 1700, easing = LinearEasing))
    }

    Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxWidth().height(170.dp)) {
        Canvas(modifier = Modifier.fillMaxWidth().height(170.dp)) {
            val t = progress.value * 1.7f
            val origin = Offset(size.width / 2f, size.height * 0.62f)
            val fade = ((1f - progress.value) / 0.25f).coerceIn(0f, 1f)

            confetti.forEach { piece ->
                val x = origin.x + cos(piece.angleRadians) * piece.speed * t
                val y = origin.y + sin(piece.angleRadians) * piece.speed * t + 900f * t * t
                if (y > size.height + 40f) return@forEach

                rotate(degrees = piece.spin * t * 60f, pivot = Offset(x, y)) {
                    drawRect(
                        color = piece.color.copy(alpha = fade),
                        topLeft = Offset(x - piece.width / 2f, y - piece.height / 2f),
                        size = Size(piece.width, piece.height),
                    )
                }
            }
        }

        // Liczba dni wjeżdża skalowaniem: pierwsze 30% animacji to powiększenie z zapasem,
        // reszta osiada na docelowym rozmiarze.
        val scale = when {
            progress.value < 0.3f -> 0.4f + (progress.value / 0.3f) * 0.75f
            else -> 1.15f - ((progress.value - 0.3f) / 0.7f) * 0.15f
        }
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = "${streak.days}",
                style = MaterialTheme.typography.displayLarge,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.graphicsLayer(scaleX = scale, scaleY = scale),
            )
            Text(
                text = if (streak.days == 1) "dzień z rzędu" else "dni z rzędu",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun FinishedScreen(
    state: UiState.Finished,
    onAgain: () -> Unit,
    onMenu: () -> Unit,
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
    ) {
        // Swietujemy tylko pierwsza ukonczona sesje danego dnia: druga i kolejna nie
        // przedluzaja serii, wiec fajerwerki bylyby wtedy klamstwem.
        if (state.streak.extendedToday) {
            StreakCelebration(state.streak)
            Text(
                text = when {
                    state.streak.days == 1 -> "Seria zaczęta."
                    state.streak.days == state.streak.best -> "Nowy rekord."
                    else -> "Seria utrzymana."
                },
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        } else {
            Text(text = "Koniec sesji", style = MaterialTheme.typography.headlineSmall)
            StreakLine(state.streak)
        }

        state.topic?.let { topic ->
            Text(
                text = topic,
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        Text(
            text = "${state.correct} / ${state.total}",
            style = MaterialTheme.typography.displaySmall,
        )
        Button(onClick = onAgain, modifier = Modifier.fillMaxWidth()) {
            Text(if (state.topic == null) "Jeszcze raz" else "Jeszcze raz w tym temacie")
        }
        OutlinedButton(onClick = onMenu, modifier = Modifier.fillMaxWidth()) {
            Text("Menu")
        }
    }
}
