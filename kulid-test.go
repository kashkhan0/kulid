package ulid

import (
	"testing"
	"time"
)

func TestmkTime(t *testing.T) {
	var (
		ulid   ULID
		tfloat = time.Unix(1469918220, 538000000)
	)
	millis := tfloat.UnixNano() / int64(time.Millisecond)
	if millis != 1469918220538 {
		t.Fatalf("mkTime fail %v not 1469918220538", millis)
	}
	mkTime(&ulid, tfloat)
	et := ulid.String()
	if et[:10] != "01aryz847t" {
		t.Fatalf("mkTime fail  got %s not '01aryz847t' ", et[:10])
	}
}

func TestmkRandom(t *testing.T) {
	var (
		ulid   ULID
		tfloat = time.Unix(1469918176, 538000000)
	)
	millis := tfloat.UnixNano() / int64(time.Millisecond)
	if millis != 1469918176538 {
		t.Fatalf("expected 1469918176538 not '%v'", millis)
	}
	mkRandom(&ulid)
	mkTime(&ulid, tfloat)
	et := ulid.String()
	if et[:10] != "01aryz847t" {
		t.Fatalf("expected 01aryz847t not %s", et[:10])
	}
}
