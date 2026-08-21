package pl.leetcodingo.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
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
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import pl.leetcodingo.data.Answer
import pl.leetcodingo.data.Exercise
import pl.leetcodingo.session.SessionViewModel
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

                is UiState.Running -> RunningScreen(
                    state = current,
                    onPick = viewModel::pick,
                    onSubmit = viewModel::submit,
                    onNext = viewModel::next,
                )

                is UiState.Finished -> FinishedScreen(current, onAgain = viewModel::start)
            }
        }
    }
}

@Composable
private fun RunningScreen(
    state: UiState.Running,
    onPick: (Int) -> Unit,
    onSubmit: () -> Unit,
    onNext: () -> Unit,
) {
    val exercise = state.exercise
    val scroll = rememberScrollState()

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
            )

            SpecCard(exercise.spec)

            Text(text = exercise.prompt, style = MaterialTheme.typography.titleMedium)

            if (exercise.code.isNotBlank()) {
                CodeBlock(exercise.code)
            }

            exercise.options.forEachIndexed { index, option ->
                OptionRow(
                    text = option,
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
 * Kod zawija sie zamiast przewijac w poziomie. Przy przewijaniu zmutowana linia
 * potrafi wyladowac poza ekranem, a cwiczenie polega wlasnie na jej zauwazeniu -
 * nic w kodzie nie moze byc schowane.
 */
@Composable
private fun CodeBlock(code: String) {
    Surface(
        color = MaterialTheme.colorScheme.surfaceContainerHighest,
        shape = RoundedCornerShape(8.dp),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Text(
            text = code,
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
            lineHeight = 17.sp,
            modifier = Modifier.padding(12.dp),
        )
    }
}

@Composable
private fun OptionRow(
    text: String,
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
            fontFamily = FontFamily.Monospace,
            style = MaterialTheme.typography.bodySmall,
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
private fun FinishedScreen(state: UiState.Finished, onAgain: () -> Unit) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.padding(24.dp),
    ) {
        Text(text = "Koniec sesji", style = MaterialTheme.typography.headlineSmall)
        Text(
            text = "${state.correct} / ${state.total}",
            style = MaterialTheme.typography.displaySmall,
        )
        Button(onClick = onAgain) { Text("Jeszcze raz") }
    }
}
