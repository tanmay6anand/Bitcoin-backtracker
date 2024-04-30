import java.util.ArrayList;
import java.util.List;

public class ApplicationManager {
    private List<String> openedApps;

    public ApplicationManager() {
        openedApps = new ArrayList<>();
    }

    public void executeCommand(String command) {
        if (command.equals("clear")) {
            clear();
        } else if (command.startsWith("open ")) {
            String appName = command.split(" ")[1];
            open(appName);
        } else if (command.startsWith("close ")) {
            int numToClose = Integer.parseInt(command.split(" ")[1]);
            close(numToClose);
        }
    }

    public void open(String appName) {
        openedApps.add(appName);
    }

    public void close(int numToClose) {
        if (numToClose >= openedApps.size()) {
            clear();
        } else {
            int numToRemove = Math.min(numToClose, openedApps.size());
            openedApps.subList(openedApps.size() - numToRemove, openedApps.size()).clear();
        }
    }

    public void clear() {
        openedApps.clear();
    }

    public List<String> getOpenedApps() {
        return openedApps;
    }
}
