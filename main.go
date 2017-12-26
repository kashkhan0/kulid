package main

import (
	"crypto/rand"
	"encoding/binary"
	"log"
	"time"
)

// 26 byte length
type ULID [16]byte

const (
	// Crockford"s Base32 in lowercase https://en.wikipedia.org/wiki/Base32
	abc               = "0123456789abcdefghjkmnpqrstvwxyz"
	abcSize           = int64(len(abc))
	encodedTimeLength = 10
	encodedRandLength = 16
)

var (
	// random
	rander = rand.Reader
	// Nil to handle errors
	Nil ULID
)

func mkulid() ULID {
	var (
		ulid ULID
	)
	err := mkRandom(&ulid)
	if err != nil {
		return Nil
	}
	mkTime(&ulid, time.Now())
	return ulid
}

func mkTime(ulid *ULID, t time.Time) {
	var x, y byte
	timestamp := uint64(t.UnixNano() / int64(time.Millisecond))
	x, y, ulid[6], ulid[7] = ulid[6], ulid[7], x, y
	binary.LittleEndian.PutUint64(ulid[:], timestamp)
	ulid[6], ulid[7] = x, y
}

func mkRandom(ulid *ULID) (err error) {
	_, err = rand.Read(ulid[6:])
	return
}

func (ulid ULID) String() string {
	var (
		buf  [26]byte
		x, y byte
	)
	// copy
	x, y, ulid[6], ulid[7] = ulid[6], ulid[7], x, y
	timestamp := int64(binary.LittleEndian.Uint64(ulid[:8]))
	ulid[6], ulid[7] = x, y
	for x := encodedTimeLength - 1; x >= 0; x-- {
		mod := timestamp % abcSize
		buf[x] = abc[mod]
		timestamp = (timestamp - mod) / abcSize
	}
	for x := encodedTimeLength; x < len(ulid); x++ {
		buf[x] = abc[int64(ulid[x])%abcSize]
	}
	return string(buf[:])
}

func main() {

	ulid := mkulid()
	log.Printf("ulid %s", ulid)

}
