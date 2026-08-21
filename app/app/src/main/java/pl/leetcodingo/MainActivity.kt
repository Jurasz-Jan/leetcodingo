package pl.leetcodingo

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.viewmodel.compose.viewModel
import pl.leetcodingo.session.SessionViewModel
import pl.leetcodingo.ui.SessionScreen
import pl.leetcodingo.ui.theme.LeetcodingoTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            LeetcodingoTheme {
                val viewModel: SessionViewModel = viewModel()
                SessionScreen(viewModel)
            }
        }
    }
}
