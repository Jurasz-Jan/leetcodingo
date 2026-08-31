package pl.leetcodingo.ui

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
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import pl.leetcodingo.data.Answer
import pl.leetcodingo.data.Exercise
import pl.leetcodingo.session.SessionViewModel
import pl.leetcodingo.session.Topic
import pl.leetcodingo.session.UiState

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

                is UiState.Running -> RunningScreen(
                    state = current,
                    onPick = viewModel::pick,
                    onSubmit = viewModel::submit,
                    onNext = viewModel::next,
                    onMenu = viewModel::openMenu,
                )

                is UiState.Finished -> FinishedScreen(
                    state = current,
                    onAgain = viewModel::again,
                    onMenu = viewModel::openMenu,
                )
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
            text = "Jeden wzorzec na całą sesję. Liczba w nawiasie to ćwiczenia jeszcze niewidziane.",
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
                        if (showPattern) append("  ·  ${exercise.pattern}")
                        append("  ·  trudność ${exercise.difficulty}")
                    },
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.weight(1f),
                )
                TextButton(onClick = onMenu) { Text("Menu") }
            }

            SpecCard(exercise.spec)

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

        Button(
            onClick = if (state.revealed) onNext else onSubmit,
            enabled = state.revealed || state.canSubmit,
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
        ) {
            Text(if (state.revealed) "Dalej" else "Sprawdź")
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

@Composable
private fun SpecCard(spec: String) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant,
        ),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(
                text = "CO KOD MA ROBIĆ",
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
private fun FinishedScreen(
    state: UiState.Finished,
    onAgain: () -> Unit,
    onMenu: () -> Unit,
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.padding(24.dp),
    ) {
        Text(text = "Koniec sesji", style = MaterialTheme.typography.headlineSmall)
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
