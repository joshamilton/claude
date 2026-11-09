/* claude-cleanup-runner
 *
 * Starts /bin/bash on one fixed script, waits for it, and returns its exit status.
 * This program is the only thing that is granted Full Disk Access for the
 * cleanup job, so it takes no arguments and runs nothing else.
 */
#include <spawn.h>
#include <stdio.h>
#include <sys/wait.h>

#define SHELL_PATH "/bin/bash"
#define SCRIPT_PATH "/Users/joshamilton/.local/bin/cleanup-claude-projects.sh"

extern char **environ;

int main(void)
{
    char *args[] = { SHELL_PATH, SCRIPT_PATH, NULL };
    pid_t pid;
    int status;
    int err = posix_spawn(&pid, SHELL_PATH, NULL, NULL, args, environ);

    if (err != 0) {
        fprintf(stderr, "claude-cleanup-runner: could not start %s (error %d)\n", SHELL_PATH, err);
        return 127;
    }
    if (waitpid(pid, &status, 0) < 0) {
        perror("claude-cleanup-runner: waitpid");
        return 126;
    }
    if (WIFEXITED(status)) {
        return WEXITSTATUS(status);
    }
    if (WIFSIGNALED(status)) {
        return 128 + WTERMSIG(status);
    }
    return 1;
}
