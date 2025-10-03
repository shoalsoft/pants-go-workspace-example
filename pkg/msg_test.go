package pkg

import "testing"

func TestFriendlyMessage(t *testing.T) {
	if FriendlyMessage() != "Hello World!" {
		t.Errorf("The friendly message was not very friendly.")
	}
}
