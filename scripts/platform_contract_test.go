package exercise_test

import (
	"encoding/json"
	model "github.com/cybericebox/daemon/internal/model/exercise"
	"github.com/cybericebox/daemon/internal/model/flagpattern"
	codec "github.com/cybericebox/daemon/internal/useCase/exercise"
	"math/big"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestPortableDemoArtifacts(t *testing.T) {
	root := os.Getenv("CIB_DEMO_ROOT")
	if root == "" {
		t.Fatal("CIB_DEMO_ROOT required")
	}
	for _, name := range []string{"static", "dynamic"} {
		t.Run(name, func(t *testing.T) {
			body, err := os.ReadFile(filepath.Join(root, "dist", name+".zip"))
			if err != nil {
				t.Fatal(err)
			}
			archive, err := codec.ParseExerciseArchive(body, "", codec.DefaultLimits())
			if err != nil {
				t.Fatal(err)
			}
			if len(archive.Versions) != 1 || archive.Versions[0].Status != model.VersionStatusPublished {
				t.Fatal("one published version required")
			}
			version := archive.Versions[0]
			if err := version.ValidateForPublish(); err != nil {
				data, _ := json.Marshal(version)
				t.Fatalf("publish validation: %v\n%s", err, data)
			}
			for _, task := range version.Variants[0].Tasks {
				if name == "dynamic" {
					p, err := flagpattern.Parse(task.Flag[0])
					if err != nil || !p.IsTemplate() {
						t.Fatal("dynamic flag must be a valid template", err)
					}
					if p.Cardinality().BitLen() < 97 {
						t.Fatal("at least 96 random flag bits required")
					}
					last := new(big.Int).Sub(p.Cardinality(), big.NewInt(1))
					for _, offset := range []*big.Int{big.NewInt(0), last} {
						flag, err := p.At(offset)
						if err != nil || !strings.HasPrefix(flag, "ICE{") {
							t.Fatal("flag materialization failed", err)
						}
					}
				}
				for _, attachment := range task.Attachments {
					if attachment.Name == "" || len(archive.Files[archive.FilePaths[attachment.FileID]]) == 0 {
						t.Fatal("imported static attachment is missing")
					}
				}
			}
		})
	}
	bundle, err := os.ReadFile(filepath.Join(root, "dist", "test-exercises.zip"))
	if err != nil {
		t.Fatal(err)
	}
	expanded, err := codec.ExpandExerciseArchiveBundle(bundle, "", codec.DefaultLimits())
	if err != nil || len(expanded) != 2 {
		t.Fatal("bundle must import as two exercises", err)
	}
}
