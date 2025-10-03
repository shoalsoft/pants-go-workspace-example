package submodule

import (
	"testing"

	"github.com/shoalsoft/pants-go-workspace-example/pkg"
)

func TestGoodbyeMessage(t *testing.T) {
	if pkg.GoodbyeMessage() != "Goodbye!" {
		t.Errorf("The goodbye message was incorrect.")
	}
}
